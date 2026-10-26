# Comprehensive Tableau Development Guide: Global EV Market Analytics

This guide provides step-by-step instructions for connecting Tableau Desktop to the EV dataset / database, building worksheets, configuring calculated fields, assembling the interactive executive dashboard, and creating the 5-scene Tableau Story.

---

## 1. Connecting Tableau to the Data Source

You can connect Tableau to either the **SQLite Database** or the **Prepared CSV File**:

### Option A: Direct SQLite Connection via ODBC (Recommended for Enterprise DB)
1. Open **Tableau Desktop**.
2. Under **Connect** -> **To a Server**, click **More...** -> **Other Databases (ODBC)**.
3. In the DSN dropdown, select your configured SQLite3 ODBC driver, or select **Driver: SQLite3 ODBC Driver**.
4. In the Connection Properties:
   - **Database Name**: Browse to `d:\Enhansed\DATA project\data\ev_market_analytics.db`.
5. Click **Connect** and **Sign In**.
6. Drag the `ev_market_analytics` table into the canvas.

### Option B: Connecting to Prepared CSV (Instant & Portable)
1. Open **Tableau Desktop**.
2. Under **Connect** -> **To a File**, click **Text file**.
3. Select `d:\Enhansed\DATA project\data\ev_market_data_prepared.csv`.
4. Ensure all field types are accurately detected:
   - `Model_Year`: Dimension (Discrete or Continuous Date)
   - `Annual_Sales_Units`: Measure (Sum)
   - `Total_Revenue_USD`: Measure (Sum)
   - `Driving_Range_km`: Measure (Average)
   - `Customer_Satisfaction_Score_pct`: Measure (Average)
   - `Sales_Region`, `Manufacturing_Country`: Geographic roles

---

## 2. Creating Key Calculated Fields in Tableau

Open the **Data** pane, click the down arrow next to the search box, and select **Create Calculated Field**:

### 1. `Price to Range Ratio ($/km)`
```tableau
[Base Price USD] / [Driving Range km]
```

### 2. `Fast Charge Speed (km/min)`
```tableau
[Driving Range km] / [Fast Charging Time min]
```

### 3. `5-Year TCO ($)`
```tableau
[Base Price USD] + ([Annual Maintenance Cost USD] * 5) + (([Energy Consumption kWh 100km] * 0.16) * 150 * 5)
```

### 4. `Market Share % (LOD Expression)`
```tableau
SUM([Annual Sales Units]) / SUM({FIXED [Model Year]: SUM([Annual Sales Units])}) * 100
```

### 5. `YoY Sales Growth % (Table Calculation)`
```tableau
(ZN(SUM([Annual Sales Units])) - LOOKUP(ZN(SUM([Annual Sales Units])), -1)) / 
ABS(LOOKUP(ZN(SUM([Annual Sales Units])), -1)) * 100
```

### 6. `Battery Longevity Tier`
```tableau
IF [Battery Life Cycles] >= 3500 THEN "Ultra-High Durability"
ELSEIF [Battery Life Cycles] >= 2500 THEN "High Durability"
ELSEIF [Battery Life Cycles] >= 1800 THEN "Standard Durability"
ELSE "Moderate Durability"
END
```

---

## 3. Building Individual Worksheets

### Worksheet 1: Annual Sales & Revenue Trajectory (Dual Axis)
- **Columns**: `Model_Year` (Continuous)
- **Rows**: `SUM(Annual_Sales_Units)` and `SUM(Total_Revenue_USD)`
- Right-click second pill on Rows -> **Dual Axis**. Synchronize axes if desired.
- Set first mark to **Area / Bar** and second to **Line**.

### Worksheet 2: Vehicle Category Market Share (Donut Chart)
- **Columns**: Dummy field `MIN(1)`, `MIN(1)`
- First mark: **Pie Chart**, slice angle by `SUM(Annual_Sales_Units)`, color by `Vehicle_Category`.
- Second mark: **Circle** (colored dark navy/white for hollow center).
- Right-click second mark on Columns -> **Dual Axis**.

### Worksheet 3: Leading EV Manufacturers Ranked (Bar Chart)
- **Columns**: `SUM(Annual_Sales_Units)`
- **Rows**: `Manufacturer` (Sorted descending by sales)
- **Color**: `SUM(Total_Revenue_USD)` or `Brand_Tier`
- Add `SUM(Annual_Sales_Units)` to **Label**.

### Worksheet 4: Battery Chemistry Benchmarking (Scatter Plot)
- **Columns**: `AVG(Energy_Consumption_kWh_100km)`
- **Rows**: `AVG(Driving_Range_km)`
- **Detail**: `Battery_Technology`
- **Size**: `SUM(Annual_Sales_Units)`
- **Color**: `Battery_Technology`

### Worksheet 5: Global Regional Production vs Sales (Geographic Map)
- Double-click `Sales_Region` or `Manufacturing_Country`
- Mark: **Map** or **Filled Map**
- Color: `SUM(Annual_Sales_Units)`
- Tooltip: Total Revenue, Average Infrastructure Index, Top Models

### Worksheet 6: Consumer Value Index (Range vs Base Price)
- **Columns**: `Vehicle_Category`
- **Rows**: `AVG(Driving_Range_km)` (Left axis) and `AVG(Base_Price_USD)` (Right axis)
- Mark type: Side-by-side or stacked bars.

---

## 4. Designing the Executive Dashboard

1. Click **New Dashboard** (`Ctrl + D`).
2. Set **Dashboard Size**: **Automatic** or **Fixed (1400 x 900)**.
3. Format background color to Dark Slate (`#0B0F19`) or Midnight Navy (`#0F172A`).
4. Drag a **Horizontal Container** at the top for the title header and KPI scorecards:
   - KPI 1: Total Units Sold
   - KPI 2: Total Revenue ($B)
   - KPI 3: Avg Driving Range (km)
   - KPI 4: Total CO2 Abated (M Tons)
5. Drag a **Horizontal Container** below for the Interactive Filters:
   - `Model_Year`, `Vehicle_Category`, `Battery_Technology`, `Sales_Region`, `Manufacturer`.
   - Set filters to: **Apply to Worksheets -> All Using This Data Source**.
6. Arrange worksheets in a 2x3 or 2x2 grid.
7. Configure **Dashboard Actions**:
   - Menu: **Dashboard** -> **Actions** -> **Add Action** -> **Filter**.
   - Source Sheet: Category Donut / Manufacturer Bar -> Target: All Sheets.
   - Run on: **Select**. Clearing selection shows all values.

---

## 5. Building the 5-Scene Tableau Story

1. Click **New Story** tab (`Ctrl + T`).
2. Set Story size to **1400 x 850**.
3. Create the 5 Story Points (Scenes):

### Story Point 1: The Exponential Surge (2019-2025)
- Drag **Worksheet 1 (Sales & Revenue Trajectory)** into the story canvas.
- Caption: *"The Exponential Surge: Global EV Market Expansion (2019–2025)"*
- Description box: Highlight 38% CAGR and milestone sales years.

### Story Point 2: Battery Chemistry War (LFP vs NMC vs Solid-State)
- Drag **Worksheet 4 (Battery Chemistry Benchmark)**.
- Caption: *"The Battery Chemistry War: Cost Parity vs Energy Density"*
- Description box: Analyze how LFP captured mass-market share while NMC maintained high-performance range.

### Story Point 3: Category Dominance (Electric SUVs & Buses)
- Drag **Worksheet 2 (Category Donut)** and **Worksheet 6 (Range vs Price)**.
- Caption: *"Category Dominance: The Electric SUV & Transit Revolution"*
- Description box: Discuss why SUVs account for 41%+ of revenues and buses lead per-vehicle emissions reduction.

### Story Point 4: Global Manufacturing Hubs & Supply Chains
- Drag **Worksheet 5 (Geographic Map)**.
- Caption: *"Manufacturing Hubs: Asia-Pacific Dominance & Regional Corridors"*
- Description box: Contrast domestic production volumes with global export flows.

### Story Point 5: Sustainability Horizon & Net-Zero Economics
- Drag KPI scorecards, Carbon Abatement summary, and TCO benchmarks.
- Caption: *"Sustainability Horizon: Lifetime Carbon Displacement & TCO"*
- Description box: Conclude with long-term emissions abatements and ROI for corporate fleet buyers.

---

## 6. Publishing and Web Embedding

1. Click **Server** -> **Tableau Public** -> **Save to Tableau Public As...**
2. Name the workbook: `ElectricVehicleMarketAnalytics`.
3. After publishing, click the **Share** icon on your Tableau Public dashboard to copy the embed link or embed code.
4. Paste the URL into the Flask Web Application at `/tableau-embed` to seamlessly display your live Tableau dashboards!
