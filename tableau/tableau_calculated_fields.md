# Tableau Calculated Fields & Measures Reference Catalog

This document details the exact calculated fields, formulas, LOD expressions, and business logic created for the EV Market Analytics project.

---

## 1. Consumer Value & Economic Efficiency

### Field 1: `Price per Range km ($/km)`
* **Formula:**
  ```tableau
  [Base Price USD] / [Driving Range km]
  ```
* **Description:** Measures capital efficiency per kilometer of driving range delivered. Lower values denote superior consumer value.
* **Target Stakeholder:** Emily Johnson & David Chen.

### Field 2: `Fast Charge Speed (km/min)`
* **Formula:**
  ```tableau
  [Driving Range km] / [Fast Charging Time min]
  ```
* **Description:** Quantifies vehicle charging convenience by computing how many kilometers of range are replenished per minute of fast charging.
* **Target Stakeholder:** Dr. Sarah Williams.

### Field 3: `Energy Cost per 100 km ($)`
* **Formula:**
  ```tableau
  [Energy Consumption kWh 100km] * 0.16
  ```
* **Description:** Computes actual fuel cost per 100 km assuming benchmark average industrial/residential electricity pricing of $0.16 per kWh.
* **Target Stakeholder:** Fleet Buyers & Emily Johnson.

### Field 4: `5-Year Total Cost of Ownership (TCO)`
* **Formula:**
  ```tableau
  [Base Price USD] + 
  ([Annual Maintenance Cost USD] * 5) + 
  (([Energy Consumption kWh 100km] * 0.16) * 150 * 5)
  ```
* **Description:** Models cumulative total cost of ownership over 5 years (75,000 km driving distance) including acquisition, recurring scheduled maintenance, and electricity costs.
* **Target Stakeholder:** Strategic Planning & Enterprise Fleet Directors.

---

## 2. Market Share & Analytical LOD Expressions

### Field 5: `Annual Global Market Share % (LOD Expression)`
* **Formula:**
  ```tableau
  SUM([Annual Sales Units]) / SUM({FIXED [Model Year]: SUM([Annual Sales Units])}) * 100
  ```
* **Description:** Level of Detail (LOD) expression that computes the exact percentage market share of a manufacturer or category relative to total global deliveries within that specific model year, regardless of other dashboard dimension slices.
* **Target Stakeholder:** David Chen.

### Field 6: `Manufacturer Revenue Share % (LOD Expression)`
* **Formula:**
  ```tableau
  SUM([Total Revenue USD]) / SUM({FIXED [Model Year]: SUM([Total Revenue USD])}) * 100
  ```
* **Description:** Calculates dollar market share against total industry turnover per calendar year.
* **Target Stakeholder:** David Chen & Executive Board.

### Field 7: `YoY Volume Growth Rate % (Table Calculation)`
* **Formula:**
  ```tableau
  (ZN(SUM([Annual Sales Units])) - LOOKUP(ZN(SUM([Annual Sales Units])), -1)) / 
  ABS(LOOKUP(ZN(SUM([Annual Sales Units])), -1)) * 100
  ```
* **Description:** Computes year-over-year unit delivery growth rate across time periods for individual automakers or vehicle segments.
* **Target Stakeholder:** Emily Johnson.

---

## 3. Sustainability & Decarbonization Metrics

### Field 8: `Carbon Abatement Efficiency (kg CO2 / $)`
* **Formula:**
  ```tableau
  ([Carbon Emissions Saved Tons] * 1000) / ([Annual Sales Units] * [Base Price USD])
  ```
* **Description:** Measures the environmental return on investment (greenhouse gas kilograms abated per dollar invested in vehicle acquisition).
* **Target Stakeholder:** Dr. Sarah Williams.

### Field 9: `Lifetime Carbon Offset Potential (Tons CO2)`
* **Formula:**
  ```tableau
  [Carbon Emissions Saved Tons] * ([Warranty Years] / 1.0)
  ```
* **Description:** Projects total cumulative lifetime emissions displacement over the vehicle's warrantied operational lifespan.
* **Target Stakeholder:** Clean Transportation Policymakers.

---

## 4. Categorical Classifications & Business Rules

### Field 10: `Battery Longevity Tier`
* **Formula:**
  ```tableau
  IF [Battery Life Cycles] >= 3500 THEN "Ultra-High Durability (>3,500 Cycles)"
  ELSEIF [Battery Life Cycles] >= 2500 THEN "High Durability (2,500-3,500 Cycles)"
  ELSEIF [Battery Life Cycles] >= 1800 THEN "Standard Commercial (1,800-2,500 Cycles)"
  ELSE "Consumer Standard (<1,800 Cycles)"
  END
  ```

### Field 11: `Range Performance Segment`
* **Formula:**
  ```tableau
  IF [Driving Range km] >= 600 THEN "Ultra-Long Range (600+ km)"
  ELSEIF [Driving Range km] >= 450 THEN "Long Range (450-599 km)"
  ELSEIF [Driving Range km] >= 300 THEN "Mid-Range Urban (300-449 km)"
  ELSE "City Commuter (<300 km)"
  END
  ```

### Field 12: `Satisfaction Health Index`
* **Formula:**
  ```tableau
  IF [Customer Satisfaction Score pct] >= 90 THEN "Exceptional (>= 90%)"
  ELSEIF [Customer Satisfaction Score pct] >= 80 THEN "Satisfactory (80-89%)"
  ELSE "Underperforming (< 80%)"
  END
  ```
