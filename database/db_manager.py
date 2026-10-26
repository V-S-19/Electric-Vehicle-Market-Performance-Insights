"""
Database Manager for EV Market Analytics
Handles SQLite schema generation, CSV ingestion, Star-Schema normalization,
analytical query execution, and performance testing benchmarks.
"""

import os
import sqlite3
import time
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "ev_market_analytics.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "ev_market_data.csv")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")
SQL_OPS_PATH = os.path.join(BASE_DIR, "database", "sql_operations.sql")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_database():
    print(f"Initializing database at: {DB_PATH}")
    conn = get_connection()
    cursor = conn.cursor()

    # Read and execute schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()
    print("Schema initialized successfully.")
    conn.close()

def ingest_data():
    print(f"Ingesting CSV data from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    conn = get_connection()
    cursor = conn.cursor()

    # Rename columns to match SQL lowercase snake_case
    df_sql = df.rename(columns={
        "Record_ID": "record_id",
        "Vehicle_ID": "vehicle_id",
        "Manufacturer": "manufacturer",
        "Model_Name": "model_name",
        "Vehicle_Category": "vehicle_category",
        "Model_Year": "model_year",
        "Battery_Technology": "battery_technology",
        "Battery_Capacity_kWh": "battery_capacity_kwh",
        "Driving_Range_km": "driving_range_km",
        "Energy_Consumption_kWh_100km": "energy_consumption_kwh_100km",
        "Fast_Charging_Time_min": "fast_charging_time_min",
        "Battery_Life_Cycles": "battery_life_cycles",
        "Base_Price_USD": "base_price_usd",
        "Annual_Sales_Units": "annual_sales_units",
        "Total_Revenue_USD": "total_revenue_usd",
        "Manufacturing_Country": "manufacturing_country",
        "Sales_Region": "sales_region",
        "Customer_Rating": "customer_rating",
        "Customer_Satisfaction_Score_pct": "customer_satisfaction_score_pct",
        "Annual_Maintenance_Cost_USD": "annual_maintenance_cost_usd",
        "Carbon_Emissions_Saved_Tons": "carbon_emissions_saved_tons",
        "Charging_Infrastructure_Index": "charging_infrastructure_index",
        "Safety_Rating_Stars": "safety_rating_stars",
        "Warranty_Years": "warranty_years"
    })

    # 1. Insert into denormalized analytics table
    df_sql.to_sql("ev_market_analytics", conn, if_exists="append", index=False)
    print(f"Ingested {len(df_sql)} records into 'ev_market_analytics' table.")

    # 2. Populate Normalized Star Schema
    # dim_manufacturer
    mfg_df = df_sql[["manufacturer", "manufacturing_country"]].drop_duplicates()
    mfg_origin_map = {
        "Tesla": ("United States", "Premium"),
        "BYD": ("China", "Mass/Value"),
        "Volkswagen Group": ("Germany", "Mass/Premium"),
        "Hyundai-Kia": ("South Korea", "Mass/Value"),
        "BMW Group": ("Germany", "Luxury"),
        "Rivian": ("United States", "Premium"),
        "NIO": ("China", "Luxury"),
        "Volvo Cars": ("Sweden", "Premium"),
        "Tata Motors": ("India", "Value"),
        "Proterra": ("United States", "Commercial"),
        "Ola Electric": ("India", "Value"),
        "SAIC Motor / MG": ("China", "Mass/Value")
    }

    for mfg in df_sql["manufacturer"].unique():
        origin, tier = mfg_origin_map.get(mfg, ("Global", "Standard"))
        cursor.execute("""
            INSERT OR IGNORE INTO dim_manufacturer (manufacturer_name, origin_country, brand_tier)
            VALUES (?, ?, ?)
        """, (mfg, origin, tier))

    # dim_vehicle_category
    for cat in df_sql["vehicle_category"].unique():
        cursor.execute("INSERT OR IGNORE INTO dim_vehicle_category (category_name) VALUES (?)", (cat,))

    # dim_battery_tech
    battery_stats = df_sql.groupby("battery_technology").agg({
        "battery_life_cycles": "mean"
    }).reset_index()
    for _, row in battery_stats.iterrows():
        b_name = row["battery_technology"]
        cursor.execute("""
            INSERT OR IGNORE INTO dim_battery_tech (technology_name, lifespan_cycles_avg)
            VALUES (?, ?)
        """, (b_name, int(row["battery_life_cycles"])))

    # dim_geography
    geo_df = df_sql[["sales_region", "manufacturing_country"]].drop_duplicates()
    for _, row in geo_df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO dim_geography (sales_region, manufacturing_country)
            VALUES (?, ?)
        """, (row["sales_region"], row["manufacturing_country"]))

    conn.commit()

    # Build dimension ID lookup mappings
    cursor.execute("SELECT manufacturer_id, manufacturer_name FROM dim_manufacturer")
    mfg_map = {row[1]: row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT category_id, category_name FROM dim_vehicle_category")
    cat_map = {row[1]: row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT tech_id, technology_name FROM dim_battery_tech")
    tech_map = {row[1]: row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT geo_id, sales_region, manufacturing_country FROM dim_geography")
    geo_map = {(row[1], row[2]): row[0] for row in cursor.fetchall()}

    # Populate fact table
    fact_rows = []
    for _, r in df_sql.iterrows():
        m_id = mfg_map[r["manufacturer"]]
        c_id = cat_map[r["vehicle_category"]]
        t_id = tech_map[r["battery_technology"]]
        g_id = geo_map[(r["sales_region"], r["manufacturing_country"])]

        fact_rows.append((
            int(r["record_id"]), r["vehicle_id"], r["model_name"], m_id, c_id, t_id, g_id,
            int(r["model_year"]), float(r["battery_capacity_kwh"]), float(r["driving_range_km"]),
            float(r["energy_consumption_kwh_100km"]), int(r["fast_charging_time_min"]),
            int(r["battery_life_cycles"]), int(r["base_price_usd"]), int(r["annual_sales_units"]),
            int(r["total_revenue_usd"]), float(r["customer_rating"]), float(r["customer_satisfaction_score_pct"]),
            int(r["annual_maintenance_cost_usd"]), float(r["carbon_emissions_saved_tons"]),
            int(r["charging_infrastructure_index"]), int(r["safety_rating_stars"]), int(r["warranty_years"])
        ))

    cursor.executemany("""
        INSERT INTO fact_ev_records VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, fact_rows)
    conn.commit()
    print(f"Populated Star Schema: {len(fact_rows)} records in 'fact_ev_records'.")
    conn.close()

def benchmark_sql_operations():
    """Runs performance testing on database queries and prints execution speeds"""
    print("\n--- PERFORMANCE TESTING BENCHMARKS ---")
    conn = get_connection()
    cursor = conn.cursor()

    queries = [
        ("Total Record Count Verification", "SELECT COUNT(*) FROM ev_market_analytics"),
        ("Scenario 1 (Emily) - Category Sales Share", """
            SELECT vehicle_category, SUM(annual_sales_units) as total_units, SUM(total_revenue_usd) as total_rev
            FROM ev_market_analytics GROUP BY vehicle_category ORDER BY total_units DESC
        """),
        ("Scenario 2 (David) - Mfg Market Share by Year", """
            SELECT model_year, manufacturer, SUM(annual_sales_units) AS units
            FROM ev_market_analytics GROUP BY model_year, manufacturer ORDER BY model_year DESC, units DESC
        """),
        ("Scenario 3 (Sarah) - Battery Tech Comparison", """
            SELECT battery_technology, AVG(driving_range_km), AVG(energy_consumption_kwh_100km), AVG(fast_charging_time_min)
            FROM ev_market_analytics GROUP BY battery_technology
        """),
        ("Filter Utilization Benchmark - Multi-condition query", """
            SELECT * FROM ev_market_analytics 
            WHERE model_year >= 2022 AND vehicle_category = 'SUV' AND battery_technology = 'LFP'
        """)
    ]

    results = []
    for name, query in queries:
        t0 = time.perf_counter()
        cursor.execute(query)
        rows = cursor.fetchall()
        t1 = time.perf_counter()
        elapsed_ms = (t1 - t0) * 1000.0
        results.append({
            "Query Description": name,
            "Row Count Returned": len(rows),
            "Execution Time (ms)": round(elapsed_ms, 3)
        })
        print(f"[OK] {name:<45} -> {len(rows):>5} rows in {elapsed_ms:>6.2f} ms")

    conn.close()
    return pd.DataFrame(results)

if __name__ == "__main__":
    init_database()
    ingest_data()
    perf_df = benchmark_sql_operations()
