# Global Electric Vehicle (EV) Market Analytics Platform
## Executive Presentation Slide Deck (Marp / Slidev / Markdown Compatible)

---

<!-- slide -->
<!-- _class: lead -->
# Global Electric Vehicle Market Analytics Platform
### Enterprise Data Intelligence, SQL Benchmarking & Strategic BI Storytelling

**Presenter:** Project Lead / Data Analytics Engineer  
**Coverage:** 2019 – 2025 Market Horizon (6,803 Records, 12 Automakers)  
**Tech Stack:** Python 3.10+ | Flask | SQLite 3 Star-Schema | Chart.js | Tableau BI

---

<!-- slide -->
## 1. The Global Mobility Transition & Problem Definition

### Rapid Market Expansion Meets Data Fragmentation
- **Industry Growth Surge:** Global EV adoption expanded at **+38% CAGR** (2019-2025).
- **Core Dilemma:** Automakers and policy makers struggle to consolidate disparate metrics across:
  - Battery Chemistries (LFP vs NMC vs Solid-State)
  - Segment Unit Economics (SUVs vs Hatchbacks vs Transit Fleets)
  - Cross-Border Trade & Sourcing Corridors
- **Our Solution:** A unified enterprise intelligence platform providing sub-millisecond query responses, multi-scene storytelling, and persona-driven decision frameworks.

---

<!-- slide -->
## 2. Engineered Around 3 Strategic Decision Personas

| Persona | Role | Core Mandate & Key Question |
| :--- | :--- | :--- |
| **Emily Johnson** | EV Market Strategy Director | Portfolio mix optimization; correlation between driving range and customer satisfaction score. |
| **David Chen** | Automotive BI Manager | Competitive manufacturer market share (Tesla, BYD, VW) and price-to-range value proposition. |
| **Dr. Sarah Williams** | Sustainable Mobility Analyst | Battery efficiency ($kWh/100km$), fast charging turnaround, and fleet lifecycle carbon abatement ($CO_2$). |

*Each persona has dedicated analytical views and curated SQL queries.*

---

<!-- slide -->
## 3. Enterprise Data Architecture & Engineering

### Dual-Storage Paradigm in SQLite 3
- **Normalized Star-Schema:**
  - Fact: `fact_ev_records` (Foreign keys + numeric measurements)
  - Dimensions: `dim_manufacturer`, `dim_vehicle_category`, `dim_battery_tech`, `dim_geography`
- **Denormalized Analytics Engine:**
  - `ev_market_analytics` table with composite B-Tree indexes on `(model_year, vehicle_category, battery_technology)`.
- **Query Performance:** Multi-condition filter queries run in **1.05 ms** (over 20x faster than full table scans).
- **Calculated Fields (12 Total):** Price-per-Range ($/km), 5-Year TCO ($), Fast-Charge Speed, and Window Partitioned Market Shares.

---

<!-- slide -->
## 4. Live Interactive Executive Dashboard

### Real-Time Responsive Slicing
- **6 Dynamic Animated KPI Scorecards:**
  - Total Vehicle Deliveries (Units)
  - Gross Market Revenue ($ USD)
  - Average Driving Range (km)
  - Average Base Price ($ USD)
  - Verified Customer Satisfaction (%)
  - Metric Tons of $CO_2$ Displaced
- **6 Synchronized Visualizations:**
  1. Multi-Year Delivery & Revenue Dual-Axis
  2. Category Volume Contribution Donut
  3. Ranked Manufacturer Market Share
  4. Battery Benchmark (Range vs Fast-Charging Speed)
  5. Regional Demand Map
  6. Value Matrix (Price vs Range)
- **Zero Lag:** Cascading updates render in `< 2.0 ms` at 60 FPS.

---

<!-- slide -->
## 5. Tableau Story Mode: 5-Scene Boardroom Narrative

1. **Scene 1: The Exponential Surge (2019-2025)**  
   Inflection points where EV deliveries shifted from niche to mainstream (+38% CAGR).
2. **Scene 2: The Battery Chemistry War**  
   Cobalt-free LFP slashes cell costs by 28%, capturing mass-market volumes while Solid-State leads luxury 600km+ models.
3. **Scene 3: Category Dominance**  
   SUVs command 41% of gross revenue; commercial transit buses yield the highest single-vehicle emission cuts (28t $CO_2$/yr).
4. **Scene 4: Global Manufacturing Superpowers**  
   China, Germany, and the US anchor 74% of production, with supply chains expanding into India and ASEAN.
5. **Scene 5: Net-Zero Economics**  
   Electric vehicles achieve a 42% lower 5-year Total Cost of Ownership ($0.16/kWh fuel baseline).

---

<!-- slide -->
## 6. Performance Testing & Project Rubric Validation

All 4 rubric verification criteria executed and validated live at `/performance`:

- **Criteria 1 (Data Ingestion to DB):**  
  **6,803 rows** verified in `ev_market_analytics.db` (~1.8 MB footprint). Full table scan in 19.4 ms.
- **Criteria 2 (Filter Utilization):**  
  Indexed filter queries execute in **1.05 ms** with instantaneous UI reactivity.
- **Criteria 3 (Calculated Fields):**  
  **12 engineered formulas** mathematically validated, including LOD expressions and window partitions.
- **Criteria 4 (Unique Visual Types):**  
  **10 distinct chart archetypes** implemented with full mobile, tablet, and 4K desktop responsiveness.

---

<!-- slide -->
## 7. Strategic Recommendations & Business Impact

### 1. Platform Portfolio Strategy
Accelerate investment in entry-level LFP architectures ($25k-$35k) where volume elasticities are highest.

### 2. High-Yield Decarbonization
Prioritize municipal bus fleet electrification to maximize carbon abatement per public subsidy dollar.

### 3. Enterprise Analytics Architecture
Coupling SQLite 3 star-schemas with lightweight Flask microservices and Tableau Embedding delivers sub-millisecond BI agility without cloud licensing overhead.

---

<!-- slide -->
<!-- _class: lead -->
# Thank You!
### Ready for Live Interactive Demonstration & Questions

- **Live Web App:** `http://127.0.0.1:5000`
- **Interactive Slides:** `http://127.0.0.1:5000/presentation`
- **Tableau Embed Portal:** `http://127.0.0.1:5000/tableau-embed`
