"""
Data Preparation & Feature Engineering Pipeline for EV Market Analytics
Handles data validation, calculated field creation, statistical profiling,
and preparation for Tableau visualizations and Web Application.
"""

import os
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, "data", "ev_market_data.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "ev_market_data_prepared.csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "analysis_and_prep", "eda_summary.json")

def prepare_data():
    print(f"Loading raw dataset from: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV)
    
    # 1. Validation & Data Hygiene
    initial_shape = df.shape
    null_counts = df.isnull().sum().to_dict()
    print(f"Initial shape: {initial_shape}. Checking for missing values: {sum(null_counts.values())} nulls found.")
    
    # Remove any duplicate rows if present
    df = df.drop_duplicates()
    
    # Clean text columns
    text_cols = ["Manufacturer", "Model_Name", "Vehicle_Category", "Battery_Technology", "Manufacturing_Country", "Sales_Region"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # 2. Advanced Feature Engineering & Calculated Fields
    print("Computing advanced analytical calculated fields...")

    # Calculated Field 1: Price-to-Range Ratio (USD per km) - Consumer Value Metric
    df["Price_per_Range_km"] = np.round(df["Base_Price_USD"] / df["Driving_Range_km"], 2)

    # Calculated Field 2: Fast Charging Delivery Speed (km added per minute of charge)
    df["Charge_Speed_km_per_min"] = np.round(df["Driving_Range_km"] / df["Fast_Charging_Time_min"], 2)

    # Calculated Field 3: Energy Cost per 100km (USD, based on benchmark $0.16/kWh)
    ELECTRICITY_COST_PER_KWH = 0.16
    df["Energy_Cost_100km_USD"] = np.round(df["Energy_Consumption_kWh_100km"] * ELECTRICITY_COST_PER_KWH, 2)

    # Calculated Field 4: 5-Year Total Cost of Ownership (TCO) assuming 15,000 km/year (75,000 km total)
    ANNUAL_KM = 15000
    df["TCO_5_Year_USD"] = np.round(
        df["Base_Price_USD"] + 
        (df["Annual_Maintenance_Cost_USD"] * 5) + 
        (df["Energy_Cost_100km_USD"] * (ANNUAL_KM / 100) * 5),
        2
    )

    # Calculated Field 5: Carbon Abatement Efficiency (kg CO2 saved per dollar spent)
    df["Carbon_Abatement_kg_per_USD"] = np.round(
        (df["Carbon_Emissions_Saved_Tons"] * 1000.0) / (df["Annual_Sales_Units"] * df["Base_Price_USD"]),
        4
    )

    # Calculated Field 6: Battery Longevity Distance Potential (Total lifetime km = Cycles * Range * 0.8)
    df["Battery_Lifetime_Potential_km"] = np.round(df["Battery_Life_Cycles"] * df["Driving_Range_km"] * 0.8, 0)

    # Calculated Field 7: Market Competitiveness Index (0-100 scale)
    # Min-max scaling range (0-30 pts), customer rating (0-40 pts), and price efficiency (0-30 pts)
    norm_range = (df["Driving_Range_km"] - df["Driving_Range_km"].min()) / (df["Driving_Range_km"].max() - df["Driving_Range_km"].min()) * 30
    norm_rating = (df["Customer_Rating"] - df["Customer_Rating"].min()) / (df["Customer_Rating"].max() - df["Customer_Rating"].min()) * 40
    norm_price_eff = (1 - (df["Price_per_Range_km"] - df["Price_per_Range_km"].min()) / (df["Price_per_Range_km"].max() - df["Price_per_Range_km"].min())) * 30
    df["Market_Competitiveness_Score"] = np.round(norm_range + norm_rating + norm_price_eff, 1)

    # Save prepared dataset
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved prepared dataset with {df.shape[1]} columns to: {OUTPUT_CSV}")

    # 3. Generate Analytical Summary & Profiling for UI & Personas
    summary = {
        "dataset_metadata": {
            "total_records": len(df),
            "total_columns": len(df.columns),
            "years_covered": sorted(df["Model_Year"].unique().tolist()),
            "total_units_sold": int(df["Annual_Sales_Units"].sum()),
            "total_revenue_usd": int(df["Total_Revenue_USD"].sum()),
            "total_co2_saved_tons": round(float(df["Carbon_Emissions_Saved_Tons"].sum()), 1),
            "avg_satisfaction_score": round(float(df["Customer_Satisfaction_Score_pct"].mean()), 2),
            "avg_range_km": round(float(df["Driving_Range_km"].mean()), 1)
        },
        "by_category": df.groupby("Vehicle_Category").agg({
            "Annual_Sales_Units": "sum",
            "Total_Revenue_USD": "sum",
            "Driving_Range_km": "mean",
            "Base_Price_USD": "mean",
            "Customer_Satisfaction_Score_pct": "mean",
            "Carbon_Emissions_Saved_Tons": "sum"
        }).round(2).to_dict(orient="index"),
        "by_battery_tech": df.groupby("Battery_Technology").agg({
            "Annual_Sales_Units": "sum",
            "Driving_Range_km": "mean",
            "Energy_Consumption_kWh_100km": "mean",
            "Fast_Charging_Time_min": "mean",
            "Battery_Life_Cycles": "mean",
            "Charge_Speed_km_per_min": "mean"
        }).round(2).to_dict(orient="index"),
        "by_manufacturer": df.groupby("Manufacturer").agg({
            "Annual_Sales_Units": "sum",
            "Total_Revenue_USD": "sum",
            "Customer_Rating": "mean",
            "Market_Competitiveness_Score": "mean"
        }).round(2).to_dict(orient="index"),
        "by_region": df.groupby("Sales_Region").agg({
            "Annual_Sales_Units": "sum",
            "Total_Revenue_USD": "sum",
            "Charging_Infrastructure_Index": "mean"
        }).round(2).to_dict(orient="index"),
        "by_year": df.groupby("Model_Year").agg({
            "Annual_Sales_Units": "sum",
            "Total_Revenue_USD": "sum",
            "Driving_Range_km": "mean",
            "Carbon_Emissions_Saved_Tons": "sum"
        }).round(2).to_dict(orient="index")
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Generated comprehensive EDA summary at: {OUTPUT_JSON}")
    return df, summary

if __name__ == "__main__":
    prepare_data()
