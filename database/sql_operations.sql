-- ============================================================================
-- SQL OPERATIONS & ANALYTICAL WORKLOADS
-- Domain: Global Electric Vehicle (EV) Industry Analysis
-- Queries specifically engineered for Emily Johnson, David Chen, and Dr. Sarah Williams
-- ============================================================================

-- ----------------------------------------------------------------------------
-- SCENARIO 1: EMILY JOHNSON — EV MARKET STRATEGY DIRECTOR
-- ----------------------------------------------------------------------------

-- Query 1.1: Vehicle Category Sales Contribution & Revenue Share per Year
-- Evaluates which vehicle categories generate the largest volume and dollar revenue
WITH TotalYearly AS (
    SELECT 
        model_year,
        SUM(annual_sales_units) AS global_sales_units,
        SUM(total_revenue_usd) AS global_revenue_usd
    FROM ev_market_analytics
    GROUP BY model_year
)
SELECT 
    e.model_year,
    e.vehicle_category,
    SUM(e.annual_sales_units) AS category_sales_units,
    ROUND(SUM(e.annual_sales_units) * 100.0 / y.global_sales_units, 2) AS sales_volume_pct,
    SUM(e.total_revenue_usd) AS category_revenue_usd,
    ROUND(SUM(e.total_revenue_usd) * 100.0 / y.global_revenue_usd, 2) AS revenue_share_pct,
    ROUND(AVG(e.base_price_usd), 0) AS avg_base_price_usd
FROM ev_market_analytics e
JOIN TotalYearly y ON e.model_year = y.model_year
GROUP BY e.model_year, e.vehicle_category, y.global_sales_units, y.global_revenue_usd
ORDER BY e.model_year DESC, category_sales_units DESC;

-- Query 1.2: Leading EV Manufacturers with YoY Volume Growth Rate (LAG Window Function)
WITH YearlyMfgSales AS (
    SELECT 
        model_year,
        manufacturer,
        SUM(annual_sales_units) AS total_units,
        SUM(total_revenue_usd) AS total_rev
    FROM ev_market_analytics
    GROUP BY model_year, manufacturer
),
YoYMetrics AS (
    SELECT 
        model_year,
        manufacturer,
        total_units,
        LAG(total_units, 1) OVER (PARTITION BY manufacturer ORDER BY model_year) AS prev_year_units,
        total_rev
    FROM YearlyMfgSales
)
SELECT 
    model_year,
    manufacturer,
    total_units,
    prev_year_units,
    CASE 
        WHEN prev_year_units IS NULL THEN 0.0
        ELSE ROUND(((total_units - prev_year_units) * 100.0 / prev_year_units), 2)
    END AS yoy_sales_growth_pct,
    RANK() OVER (PARTITION BY model_year ORDER BY total_units DESC) AS mfg_market_rank
FROM YoYMetrics
WHERE model_year >= 2021
ORDER BY model_year DESC, total_units DESC;

-- Query 1.3: Driving Range vs Customer Satisfaction Across Product Segments
SELECT 
    vehicle_category,
    battery_technology,
    COUNT(*) AS total_models_analyzed,
    ROUND(AVG(driving_range_km), 1) AS avg_driving_range_km,
    ROUND(MIN(driving_range_km), 1) AS min_range_km,
    ROUND(MAX(driving_range_km), 1) AS max_range_km,
    ROUND(AVG(customer_satisfaction_score_pct), 2) AS avg_satisfaction_score_pct,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
    ROUND(AVG(base_price_usd) / AVG(driving_range_km), 2) AS price_per_km_range
FROM ev_market_analytics
GROUP BY vehicle_category, battery_technology
ORDER BY vehicle_category, avg_satisfaction_score_pct DESC;


-- ----------------------------------------------------------------------------
-- SCENARIO 2: DAVID CHEN — AUTOMOTIVE BUSINESS INTELLIGENCE MANAGER
-- ----------------------------------------------------------------------------

-- Query 2.1: Global Manufacturer Market Share and Trajectory (Dense Rank & Partition)
WITH GlobalTotals AS (
    SELECT 
        model_year,
        SUM(annual_sales_units) AS global_units,
        SUM(total_revenue_usd) AS global_revenue
    FROM ev_market_analytics
    GROUP BY model_year
),
MfgTotals AS (
    SELECT 
        e.model_year,
        e.manufacturer,
        SUM(e.annual_sales_units) AS mfg_units,
        SUM(e.total_revenue_usd) AS mfg_revenue
    FROM ev_market_analytics e
    GROUP BY e.model_year, e.manufacturer
)
SELECT 
    m.model_year,
    m.manufacturer,
    m.mfg_units,
    ROUND(m.mfg_units * 100.0 / g.global_units, 2) AS unit_market_share_pct,
    ROUND(m.mfg_revenue * 100.0 / g.global_revenue, 2) AS revenue_market_share_pct,
    DENSE_RANK() OVER (PARTITION BY m.model_year ORDER BY m.mfg_units DESC) AS annual_rank
FROM MfgTotals m
JOIN GlobalTotals g ON m.model_year = g.model_year
WHERE m.model_year IN (2020, 2022, 2024, 2025)
ORDER BY m.model_year DESC, m.mfg_units DESC;

-- Query 2.2: Battery Technology Adoption Matrix by Manufacturer
SELECT 
    manufacturer,
    SUM(CASE WHEN battery_technology = 'LFP' THEN annual_sales_units ELSE 0 END) AS units_lfp,
    SUM(CASE WHEN battery_technology = 'NMC' THEN annual_sales_units ELSE 0 END) AS units_nmc,
    SUM(CASE WHEN battery_technology = 'NCA' THEN annual_sales_units ELSE 0 END) AS units_nca,
    SUM(CASE WHEN battery_technology = 'Sodium-Ion' THEN annual_sales_units ELSE 0 END) AS units_sodium_ion,
    SUM(CASE WHEN battery_technology = 'Solid-State' THEN annual_sales_units ELSE 0 END) AS units_solid_state,
    SUM(annual_sales_units) AS grand_total_units,
    ROUND(SUM(CASE WHEN battery_technology = 'LFP' THEN annual_sales_units ELSE 0 END) * 100.0 / SUM(annual_sales_units), 1) AS lfp_share_pct
FROM ev_market_analytics
WHERE model_year >= 2023
GROUP BY manufacturer
ORDER BY grand_total_units DESC;

-- Query 2.3: Geographical Production vs Destination Sales Analysis
SELECT 
    manufacturing_country,
    sales_region,
    COUNT(DISTINCT vehicle_id) AS distinct_vehicle_types,
    SUM(annual_sales_units) AS units_distributed,
    SUM(total_revenue_usd) AS revenue_generated_usd,
    ROUND(AVG(base_price_usd), 0) AS avg_unit_price_usd,
    ROUND(AVG(charging_infrastructure_index), 1) AS avg_infra_score
FROM ev_market_analytics
GROUP BY manufacturing_country, sales_region
ORDER BY manufacturing_country, units_distributed DESC;


-- ----------------------------------------------------------------------------
-- SCENARIO 3: DR. SARAH WILLIAMS — SUSTAINABLE MOBILITY RESEARCH ANALYST
-- ----------------------------------------------------------------------------

-- Query 3.1: Comprehensive Battery Technology Performance Benchmark
SELECT 
    battery_technology,
    COUNT(DISTINCT model_name) AS model_count,
    ROUND(AVG(driving_range_km), 1) AS avg_driving_range_km,
    ROUND(AVG(energy_consumption_kwh_100km), 2) AS avg_energy_consumption_kwh_100km,
    ROUND(AVG(fast_charging_time_min), 1) AS avg_fast_charging_mins,
    ROUND(AVG(battery_life_cycles), 0) AS avg_life_cycles,
    ROUND(AVG(base_price_usd / battery_capacity_kwh), 2) AS price_per_kwh_capacity_usd
FROM ev_market_analytics
GROUP BY battery_technology
ORDER BY avg_driving_range_km DESC;

-- Query 3.2: Environmental Impact & CO2 Reduction by Vehicle Category
SELECT 
    vehicle_category,
    SUM(annual_sales_units) AS total_ev_fleet_deployed,
    ROUND(SUM(carbon_emissions_saved_tons), 1) AS total_co2_saved_metric_tons,
    ROUND(SUM(carbon_emissions_saved_tons) / SUM(annual_sales_units), 2) AS avg_co2_saved_per_vehicle_tons,
    ROUND(SUM(annual_sales_units * annual_maintenance_cost_usd) / SUM(annual_sales_units), 0) AS avg_fleet_annual_maintenance_usd
FROM ev_market_analytics
GROUP BY vehicle_category
ORDER BY total_co2_saved_metric_tons DESC;

-- Query 3.3: Longitudinal Technological Evolution (2019 vs 2025 Benchmarking)
WITH Year2019 AS (
    SELECT 
        battery_technology,
        AVG(driving_range_km) AS avg_range_2019,
        AVG(energy_consumption_kwh_100km) AS avg_consumption_2019,
        AVG(fast_charging_time_min) AS avg_charging_2019
    FROM ev_market_analytics
    WHERE model_year = 2019
    GROUP BY battery_technology
),
Year2025 AS (
    SELECT 
        battery_technology,
        AVG(driving_range_km) AS avg_range_2025,
        AVG(energy_consumption_kwh_100km) AS avg_consumption_2025,
        AVG(fast_charging_time_min) AS avg_charging_2025
    FROM ev_market_analytics
    WHERE model_year = 2025
    GROUP BY battery_technology
)
SELECT 
    y25.battery_technology,
    ROUND(y19.avg_range_2019, 1) AS range_2019_km,
    ROUND(y25.avg_range_2025, 1) AS range_2025_km,
    ROUND(((y25.avg_range_2025 - y19.avg_range_2019) * 100.0 / y19.avg_range_2019), 1) AS range_improvement_pct,
    ROUND(y19.avg_consumption_2019, 2) AS consumption_2019,
    ROUND(y25.avg_consumption_2025, 2) AS consumption_2025,
    ROUND(y19.avg_charging_2019, 1) AS charge_mins_2019,
    ROUND(y25.avg_charging_2025, 1) AS charge_mins_2025
FROM Year2025 y25
LEFT JOIN Year2019 y19 ON y25.battery_technology = y19.battery_technology
ORDER BY range_2025_km DESC;
