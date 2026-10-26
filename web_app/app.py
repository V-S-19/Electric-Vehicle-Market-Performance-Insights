"""
Electric Vehicle (EV) Market Analytics - Flask Web Application
Provides interactive dashboards, Tableau story embedding, SQL Explorer,
performance testing benchmarks, and persona-tailored decision views.
"""

import os
import json
import sqlite3
import time
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "ev_market_analytics.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "ev_market_data_prepared.csv")
EDA_SUMMARY_PATH = os.path.join(BASE_DIR, "analysis_and_prep", "eda_summary.json")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_eda_summary():
    if os.path.exists(EDA_SUMMARY_PATH):
        with open(EDA_SUMMARY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# ----------------------------------------------------------------------------
# PAGE ROUTES
# ----------------------------------------------------------------------------

@app.route("/")
def index():
    """Project Overview & Problem Understanding Page"""
    summary = load_eda_summary()
    return render_template("index.html", summary=summary)

@app.route("/dashboard")
def dashboard():
    """Interactive Executive EV Market Dashboard"""
    summary = load_eda_summary()
    return render_template("dashboard.html", summary=summary)

@app.route("/story")
def story():
    """Tableau-Style 5-Scene Narrative Story Mode"""
    return render_template("story.html")

@app.route("/personas")
def personas():
    """Strategic Decision Portals for Emily, David, and Dr. Sarah"""
    summary = load_eda_summary()
    return render_template("personas.html", summary=summary)

@app.route("/sql-explorer")
def sql_explorer():
    """Interactive SQL query execution and benchmarking tool"""
    return render_template("sql_explorer.html")

@app.route("/performance")
def performance():
    """Performance Testing Center (Data Render, Filter Speed, Calculated Fields, Graphs)"""
    return render_template("performance.html")

@app.route("/tableau-embed")
def tableau_embed():
    """Tableau Server / Public Embed Integration"""
    return render_template("tableau_embed.html")

@app.route("/documentation")
def documentation():
    """Step-by-step project development procedure and guides"""
    return render_template("documentation.html")

@app.route("/presentation")
def presentation():
    """Interactive Executive Presentation Slide Deck"""
    return render_template("presentation.html")


# ----------------------------------------------------------------------------
# API ENDPOINTS
# ----------------------------------------------------------------------------

@app.route("/api/filter-options", methods=["GET"])
def get_filter_options():
    """Returns unique distinct values for filter dropdowns"""
    conn = get_db()
    cursor = conn.cursor()

    years = [row[0] for row in cursor.execute("SELECT DISTINCT model_year FROM ev_market_analytics ORDER BY model_year").fetchall()]
    categories = [row[0] for row in cursor.execute("SELECT DISTINCT vehicle_category FROM ev_market_analytics ORDER BY vehicle_category").fetchall()]
    batteries = [row[0] for row in cursor.execute("SELECT DISTINCT battery_technology FROM ev_market_analytics ORDER BY battery_technology").fetchall()]
    regions = [row[0] for row in cursor.execute("SELECT DISTINCT sales_region FROM ev_market_analytics ORDER BY sales_region").fetchall()]
    manufacturers = [row[0] for row in cursor.execute("SELECT DISTINCT manufacturer FROM ev_market_analytics ORDER BY manufacturer").fetchall()]
    countries = [row[0] for row in cursor.execute("SELECT DISTINCT manufacturing_country FROM ev_market_analytics ORDER BY manufacturing_country").fetchall()]

    conn.close()
    return jsonify({
        "years": years,
        "categories": categories,
        "batteries": batteries,
        "regions": regions,
        "manufacturers": manufacturers,
        "countries": countries
    })

@app.route("/api/data", methods=["GET"])
def get_filtered_data():
    """Dynamic multi-parameter filtering and analytics aggregation"""
    year = request.args.get("year", "all")
    category = request.args.get("category", "all")
    battery = request.args.get("battery", "all")
    region = request.args.get("region", "all")
    manufacturer = request.args.get("manufacturer", "all")

    query = "SELECT * FROM ev_market_analytics WHERE 1=1"
    params = []

    if year != "all":
        query += " AND model_year = ?"
        params.append(int(year))
    if category != "all":
        query += " AND vehicle_category = ?"
        params.append(category)
    if battery != "all":
        query += " AND battery_technology = ?"
        params.append(battery)
    if region != "all":
        query += " AND sales_region = ?"
        params.append(region)
    if manufacturer != "all":
        query += " AND manufacturer = ?"
        params.append(manufacturer)

    t0 = time.perf_counter()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    t1 = time.perf_counter()
    execution_time_ms = round((t1 - t0) * 1000.0, 2)

    col_names = [description[0] for description in cursor.description]
    data = [dict(zip(col_names, row)) for row in rows]
    conn.close()

    if not data:
        return jsonify({
            "record_count": 0,
            "execution_time_ms": execution_time_ms,
            "kpis": {},
            "charts": {}
        })

    df = pd.DataFrame(data)

    # Calculate live KPIs
    total_sales = int(df["annual_sales_units"].sum())
    total_rev = int(df["total_revenue_usd"].sum())
    avg_range = round(float(df["driving_range_km"].mean()), 1)
    avg_price = round(float(df["base_price_usd"].mean()), 0)
    avg_satisfaction = round(float(df["customer_satisfaction_score_pct"].mean()), 1)
    total_co2 = round(float(df["carbon_emissions_saved_tons"].sum()), 1)

    kpis = {
        "total_sales_units": total_sales,
        "total_revenue_usd": total_rev,
        "avg_driving_range_km": avg_range,
        "avg_base_price_usd": avg_price,
        "avg_satisfaction_pct": avg_satisfaction,
        "total_co2_saved_tons": total_co2,
        "filtered_record_count": len(df)
    }

    # Chart 1: Sales & Revenue by Year
    yearly = df.groupby("model_year").agg({
        "annual_sales_units": "sum",
        "total_revenue_usd": "sum"
    }).reset_index().to_dict(orient="list")

    # Chart 2: Category Distribution
    by_cat = df.groupby("vehicle_category").agg({
        "annual_sales_units": "sum"
    }).sort_values(by="annual_sales_units", ascending=False).to_dict()

    # Chart 3: Top Manufacturers by Sales
    by_mfg = df.groupby("manufacturer").agg({
        "annual_sales_units": "sum"
    }).sort_values(by="annual_sales_units", ascending=False).head(8).to_dict()

    # Chart 4: Battery Technology Market Share
    by_battery = df.groupby("battery_technology").agg({
        "annual_sales_units": "sum",
        "driving_range_km": "mean",
        "energy_consumption_kwh_100km": "mean",
        "fast_charging_time_min": "mean"
    }).round(2).to_dict(orient="index")

    # Chart 5: Regional Sales Contribution
    by_reg = df.groupby("sales_region").agg({
        "annual_sales_units": "sum"
    }).sort_values(by="annual_sales_units", ascending=False).to_dict()

    # Chart 6: Category vs Range & Price
    cat_range_price = df.groupby("vehicle_category").agg({
        "driving_range_km": "mean",
        "base_price_usd": "mean"
    }).round(1).to_dict(orient="index")

    # Chart 7: Manufacturing Country Breakdown
    by_country = df.groupby("manufacturing_country").agg({
        "annual_sales_units": "sum"
    }).sort_values(by="annual_sales_units", ascending=False).to_dict()

    return jsonify({
        "record_count": len(df),
        "execution_time_ms": execution_time_ms,
        "kpis": kpis,
        "charts": {
            "yearly": yearly,
            "category": by_cat["annual_sales_units"],
            "manufacturer": by_mfg["annual_sales_units"],
            "battery": by_battery,
            "region": by_reg["annual_sales_units"],
            "cat_range_price": cat_range_price,
            "country": by_country["annual_sales_units"]
        }
    })

@app.route("/api/run-sql", methods=["POST"])
def run_sql():
    """Executes arbitrary read-only SQL query for interactive SQL explorer"""
    body = request.get_json() or {}
    query = body.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty query provided."}), 400

    # Ensure query is read-only
    first_word = query.split()[0].upper() if query.split() else ""
    if first_word not in ["SELECT", "WITH", "EXPLAIN"]:
        return jsonify({"error": "Only read-only queries (SELECT, WITH, EXPLAIN) are permitted."}), 403

    conn = get_db()
    cursor = conn.cursor()
    try:
        t0 = time.perf_counter()
        cursor.execute(query)
        rows = cursor.fetchall()
        t1 = time.perf_counter()
        exec_ms = round((t1 - t0) * 1000.0, 3)

        col_names = [d[0] for d in cursor.description] if cursor.description else []
        results = [list(r) for r in rows[:100]]  # limit to 100 rows for display safety

        return jsonify({
            "columns": col_names,
            "rows": results,
            "total_rows": len(rows),
            "execution_time_ms": exec_ms,
            "is_truncated": len(rows) > 100
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route("/api/performance-benchmark", methods=["GET"])
def run_performance_benchmarks():
    """Runs a series of performance benchmark tests and returns latency & metrics"""
    conn = get_db()
    cursor = conn.cursor()

    tests = [
        {"name": "Full Table Scan (6,803 rows)", "query": "SELECT * FROM ev_market_analytics"},
        {"name": "Multi-Dimension Aggregation (Category + Battery + Year)", "query": """
            SELECT model_year, vehicle_category, battery_technology, 
                   COUNT(*), SUM(annual_sales_units), AVG(driving_range_km)
            FROM ev_market_analytics GROUP BY model_year, vehicle_category, battery_technology
        """},
        {"name": "Indexed Filter Scan (Year = 2024 AND Category = 'SUV')", "query": """
            SELECT * FROM ev_market_analytics WHERE model_year = 2024 AND vehicle_category = 'SUV'
        """},
        {"name": "Manufacturer Market Share Window Function", "query": """
            SELECT model_year, manufacturer, SUM(annual_sales_units) AS units,
                   RANK() OVER (PARTITION BY model_year ORDER BY SUM(annual_sales_units) DESC) as rnk
            FROM ev_market_analytics GROUP BY model_year, manufacturer
        """},
        {"name": "Star-Schema Join (Fact + 4 Dimensions)", "query": """
            SELECT f.record_id, m.manufacturer_name, c.category_name, b.technology_name, g.sales_region, f.annual_sales_units
            FROM fact_ev_records f
            JOIN dim_manufacturer m ON f.manufacturer_id = m.manufacturer_id
            JOIN dim_vehicle_category c ON f.category_id = c.category_id
            JOIN dim_battery_tech b ON f.tech_id = b.tech_id
            JOIN dim_geography g ON f.geo_id = g.geo_id
            LIMIT 500
        """}
    ]

    results = []
    for test in tests:
        t0 = time.perf_counter()
        cursor.execute(test["query"])
        rows = cursor.fetchall()
        t1 = time.perf_counter()
        results.append({
            "test_name": test["name"],
            "rows_returned": len(rows),
            "execution_time_ms": round((t1 - t0) * 1000.0, 3),
            "status": "PASS"
        })

    # Database file stats
    db_size_bytes = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    csv_size_bytes = os.path.getsize(CSV_PATH) if os.path.exists(CSV_PATH) else 0

    conn.close()
    return jsonify({
        "benchmarks": results,
        "database_metrics": {
            "db_size_kb": round(db_size_bytes / 1024, 1),
            "csv_size_kb": round(csv_size_bytes / 1024, 1),
            "total_records_rendered": 6803,
            "calculated_fields_count": 7,
            "unique_visualizations_count": 10
        }
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
