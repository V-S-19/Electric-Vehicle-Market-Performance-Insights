-- ============================================================================
-- Electric Vehicle (EV) Market Analytics - Enterprise Database Schema (DDL)
-- Database Engine: SQLite 3 / ANSI SQL Compatible
-- Author: Data Analytics Engineering Team
-- ============================================================================

-- Drop existing tables/views if they exist
DROP VIEW IF EXISTS vw_sarah_sustainable_mobility;
DROP VIEW IF EXISTS vw_david_bi_benchmarks;
DROP VIEW IF EXISTS vw_emily_market_strategy;
DROP TABLE IF EXISTS fact_ev_records;
DROP TABLE IF EXISTS dim_geography;
DROP TABLE IF EXISTS dim_battery_tech;
DROP TABLE IF EXISTS dim_vehicle_category;
DROP TABLE IF EXISTS dim_manufacturer;
DROP TABLE IF EXISTS ev_market_analytics;

-- ============================================================================
-- 1. DENORMALIZED ANALYTICS TABLE (Optimized for Tableau & BI High-Throughput)
-- ============================================================================
CREATE TABLE ev_market_analytics (
    record_id INTEGER PRIMARY KEY,
    vehicle_id TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    model_name TEXT NOT NULL,
    vehicle_category TEXT NOT NULL,
    model_year INTEGER NOT NULL,
    battery_technology TEXT NOT NULL,
    battery_capacity_kwh REAL NOT NULL,
    driving_range_km REAL NOT NULL,
    energy_consumption_kwh_100km REAL NOT NULL,
    fast_charging_time_min INTEGER NOT NULL,
    battery_life_cycles INTEGER NOT NULL,
    base_price_usd INTEGER NOT NULL,
    annual_sales_units INTEGER NOT NULL,
    total_revenue_usd INTEGER NOT NULL,
    manufacturing_country TEXT NOT NULL,
    sales_region TEXT NOT NULL,
    customer_rating REAL NOT NULL,
    customer_satisfaction_score_pct REAL NOT NULL,
    annual_maintenance_cost_usd INTEGER NOT NULL,
    carbon_emissions_saved_tons REAL NOT NULL,
    charging_infrastructure_index INTEGER NOT NULL,
    safety_rating_stars INTEGER NOT NULL,
    warranty_years INTEGER NOT NULL
);

-- ============================================================================
-- 2. NORMALIZED STAR-SCHEMA (Enterprise DW Modeling)
-- ============================================================================

CREATE TABLE dim_manufacturer (
    manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_name TEXT UNIQUE NOT NULL,
    origin_country TEXT NOT NULL,
    brand_tier TEXT NOT NULL
);

CREATE TABLE dim_vehicle_category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
);

CREATE TABLE dim_battery_tech (
    tech_id INTEGER PRIMARY KEY AUTOINCREMENT,
    technology_name TEXT UNIQUE NOT NULL,
    density_wh_kg_avg REAL,
    lifespan_cycles_avg INTEGER
);

CREATE TABLE dim_geography (
    geo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sales_region TEXT NOT NULL,
    manufacturing_country TEXT NOT NULL,
    UNIQUE(sales_region, manufacturing_country)
);

CREATE TABLE fact_ev_records (
    record_id INTEGER PRIMARY KEY,
    vehicle_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    manufacturer_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    tech_id INTEGER NOT NULL,
    geo_id INTEGER NOT NULL,
    model_year INTEGER NOT NULL,
    battery_capacity_kwh REAL NOT NULL,
    driving_range_km REAL NOT NULL,
    energy_consumption_kwh_100km REAL NOT NULL,
    fast_charging_time_min INTEGER NOT NULL,
    battery_life_cycles INTEGER NOT NULL,
    base_price_usd INTEGER NOT NULL,
    annual_sales_units INTEGER NOT NULL,
    total_revenue_usd INTEGER NOT NULL,
    customer_rating REAL NOT NULL,
    customer_satisfaction_score_pct REAL NOT NULL,
    annual_maintenance_cost_usd INTEGER NOT NULL,
    carbon_emissions_saved_tons REAL NOT NULL,
    charging_infrastructure_index INTEGER NOT NULL,
    safety_rating_stars INTEGER NOT NULL,
    warranty_years INTEGER NOT NULL,
    FOREIGN KEY (manufacturer_id) REFERENCES dim_manufacturer(manufacturer_id),
    FOREIGN KEY (category_id) REFERENCES dim_vehicle_category(category_id),
    FOREIGN KEY (tech_id) REFERENCES dim_battery_tech(tech_id),
    FOREIGN KEY (geo_id) REFERENCES dim_geography(geo_id)
);

-- ============================================================================
-- 3. INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================
CREATE INDEX idx_ev_year_cat ON ev_market_analytics (model_year, vehicle_category);
CREATE INDEX idx_ev_manufacturer ON ev_market_analytics (manufacturer);
CREATE INDEX idx_ev_battery ON ev_market_analytics (battery_technology);
CREATE INDEX idx_ev_region ON ev_market_analytics (sales_region);
CREATE INDEX idx_ev_mfg_country ON ev_market_analytics (manufacturing_country);
CREATE INDEX idx_fact_composite ON fact_ev_records (model_year, manufacturer_id, category_id);

-- ============================================================================
-- 4. ANALYTICAL VIEWS FOR SCENARIO PERSONAS
-- ============================================================================

-- Scenario 1: Emily Johnson (Market Strategy Director)
CREATE VIEW vw_emily_market_strategy AS
SELECT 
    model_year,
    vehicle_category,
    COUNT(DISTINCT model_name) AS active_models,
    SUM(annual_sales_units) AS total_units_sold,
    SUM(total_revenue_usd) AS total_revenue_usd,
    ROUND(AVG(base_price_usd), 2) AS avg_price_usd,
    ROUND(AVG(driving_range_km), 1) AS avg_range_km,
    ROUND(AVG(customer_satisfaction_score_pct), 2) AS avg_satisfaction_pct,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM ev_market_analytics
GROUP BY model_year, vehicle_category;

-- Scenario 2: David Chen (Automotive Business Intelligence Manager)
CREATE VIEW vw_david_bi_benchmarks AS
SELECT 
    model_year,
    manufacturer,
    manufacturing_country,
    battery_technology,
    SUM(annual_sales_units) AS total_sales_units,
    SUM(total_revenue_usd) AS total_revenue_usd,
    ROUND(AVG(base_price_usd), 2) AS avg_selling_price,
    ROUND(AVG(customer_rating), 2) AS avg_rating,
    ROUND(AVG(driving_range_km), 1) AS avg_range_km
FROM ev_market_analytics
GROUP BY model_year, manufacturer, manufacturing_country, battery_technology;

-- Scenario 3: Dr. Sarah Williams (Sustainable Mobility Research Analyst)
CREATE VIEW vw_sarah_sustainable_mobility AS
SELECT 
    battery_technology,
    model_year,
    ROUND(AVG(driving_range_km), 1) AS avg_range_km,
    ROUND(AVG(energy_consumption_kwh_100km), 2) AS avg_energy_eff_kwh_100km,
    ROUND(AVG(fast_charging_time_min), 1) AS avg_fast_charging_min,
    ROUND(AVG(battery_life_cycles), 0) AS avg_lifespan_cycles,
    SUM(carbon_emissions_saved_tons) AS total_co2_saved_tons,
    SUM(annual_sales_units) AS total_fleet_size
FROM ev_market_analytics
GROUP BY battery_technology, model_year;
