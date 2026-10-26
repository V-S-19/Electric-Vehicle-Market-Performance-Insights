# End-to-End Project Demonstration Video Script
## Global Electric Vehicle (EV) Market Analytics Platform
**Target Duration:** 8 – 10 Minutes  
**Audience:** Executive Stakeholders, Academic Evaluators, Business Intelligence Directors

---

## Video Scene Outline & Timestamps

| Section | Timestamp | Description | Visual Target |
| :--- | :--- | :--- | :--- |
| **Scene 1** | 00:00 – 01:15 | Project Introduction & Problem Definition | Web UI: Overview Page (`/`) |
| **Scene 2** | 01:15 – 02:30 | The 3 Personas & Business Objectives | Web UI: Personas Page (`/personas`) |
| **Scene 3** | 02:30 – 03:45 | Data Architecture, SQLite Schema & SQL Queries | VS Code / SQL Explorer (`/sql-explorer`) |
| **Scene 4** | 03:45 – 05:45 | Interactive Executive Dashboard Walkthrough | Web UI: Dashboard (`/dashboard`) |
| **Scene 5** | 05:45 – 07:15 | Tableau Story Mode: 5-Scene Narrative | Web UI: Story Mode (`/story`) |
| **Scene 6** | 07:15 – 08:30 | Performance Testing & Rubric Verification | Web UI: Performance (`/performance`) |
| **Scene 7** | 08:30 – 09:30 | Tableau Embed & Flask Architecture | Web UI: Tableau Embed & Codebase |
| **Scene 8** | 09:30 – 10:00 | Conclusion & Strategic Recommendations | Slide / Camera Summary |

---

## Detailed Spoken Script

### Scene 1: Project Introduction & Problem Definition (00:00 – 01:15)
* **[Screen:]** Open the browser to the Flask Web Application at `http://127.0.0.1:5000/`.
* **[Speaker Audio:]**
  > "Hello everyone, and welcome to the comprehensive walkthrough of our Global Electric Vehicle Market Analytics Platform.
  > 
  > The electric vehicle industry is currently navigating the most pivotal shift in automotive history. Driven by carbon reduction targets, government incentives, and rapid advances in battery technology, the EV sector is expanding across passenger cars, commercial transport, and urban two-wheelers.
  > 
  > However, this explosive growth produces massive amounts of complex data across pricing, battery specifications, sales figures, and manufacturing distribution. To help leaders make sense of this data, we have engineered an end-to-end analytical solution—combining a robust multi-dimensional dataset of over 6,800 records, a high-performance SQLite database, advanced SQL analytical queries, interactive Tableau dashboards and stories, and a modern Flask web application."

---

### Scene 2: The Three Strategic Personas (01:15 – 02:30)
* **[Screen:]** Navigate to `/personas` and highlight the three persona cards.
* **[Speaker Audio:]**
  > "To ensure our analytics deliver real business value, we formulated our architecture around three core industry personas:
  > 
  > First, **Emily Johnson**, EV Market Strategy Director for a global automaker. Emily needs executive insights into category contributions, battery adoption curves, and customer satisfaction across vehicle segments to guide multi-billion dollar platform investments.
  > 
  > Second, **David Chen**, Automotive Business Intelligence Manager at a global consulting firm. David focuses on competitive market share, geographical production hubs versus export destinations, and brand positioning to help clients expand into new markets.
  > 
  > Third, **Dr. Sarah Williams**, Sustainable Mobility Research Analyst at a clean energy institute. Dr. Sarah evaluates battery chemistry performance—such as LFP versus NMC versus next-generation Solid-State—energy consumption in kilowatt-hours per 100 kilometers, and cumulative greenhouse gas abatement."

---

### Scene 3: Data Architecture, SQLite Schema & SQL Queries (02:30 – 03:45)
* **[Screen:]** Navigate to `/sql-explorer` and show `database/schema.sql` and `database/sql_operations.sql`.
* **[Speaker Audio:]**
  > "Let's examine the underlying data engineering. Our data model is stored in an enterprise SQLite 3 database named `ev_market_analytics.db`.
  > 
  > We implemented a dual-schema design: an enterprise star-schema with a central fact table—`fact_ev_records`—linked to dimension tables for manufacturers, vehicle categories, battery technologies, and geographies. Additionally, we maintained a high-throughput denormalized table `ev_market_analytics` indexed with B-Trees for instantaneous dashboard queries.
  > 
  > In our interactive SQL Explorer, we can directly run analytical queries. Let's click on Emily's preset query demonstrating category sales and revenue by year... notice the execution latency is just 3 milliseconds!
  > 
  > We also utilize Common Table Expressions, Window Functions like `RANK()`, `DENSE_RANK()`, and `LAG()` to calculate year-over-year growth and global market share in real time."

---

### Scene 4: Interactive Executive Dashboard (03:45 – 05:45)
* **[Screen:]** Navigate to `/dashboard`. Demonstrate toggling filters (e.g. Model Year = 2024, Vehicle Category = SUV, Battery = LFP).
* **[Speaker Audio:]**
  > "Now, let's step into the Executive EV Market Intelligence Dashboard.
  > 
  > The dashboard features a modern, responsive dark glassmorphism design with six real-time KPI scorecards displaying Total Deliveries, Gross Revenue, Average Driving Range, Average Selling Price, Verified Customer Satisfaction, and Total Metric Tons of CO2 abated.
  > 
  > At the top, we have a multi-parameter filter bar. Watch what happens when I filter the data for the year 2024 and select the 'SUV' category...
  > 
  > In less than 2 milliseconds, all KPI numbers animate to reflect the filtered slice, and our six synchronized charts update immediately:
  > 1. Our dual-axis line chart shows the trajectory of sales units and dollar revenue.
  > 2. The category donut chart illustrates market volume share.
  > 3. The ranked bar chart benchmarks leading automakers like Tesla, BYD, and Volkswagen.
  > 4. The battery benchmark compares driving range against fast-charging turnaround.
  > 5. The regional map breaks down demand across Asia-Pacific, Europe, and North America.
  > 6. And the value proposition chart contrasts range with base vehicle price."

---

### Scene 5: Tableau Story Mode — 5 Narrative Scenes (05:45 – 07:15)
* **[Screen:]** Navigate to `/story`. Click through Scene 1 to Scene 5.
* **[Speaker Audio:]**
  > "Next, we present the interactive Tableau Story Mode, organized into five sequential narrative scenes designed for board-level presentations:
  > 
  > - **Scene 1: The Exponential Surge (2019–2025):** Details the 38% compound annual growth rate and the inflection point where EVs reached mass adoption.
  > - **Scene 2: Battery Chemistry War:** Examines how Lithium Iron Phosphate (LFP) emerged as the dominant chemistry for mass-market vehicles, slashing cell costs by 28%, while NMC and Solid-State lead the luxury range frontier.
  > - **Scene 3: Category Dominance:** Analyzes why SUVs capture over 41% of global EV revenue, while electric transit buses deliver the highest per-vehicle carbon reduction—up to 28 tons of CO2 annually per bus.
  > - **Scene 4: Global Manufacturing Superpowers:** Maps production concentration in China, Germany, and the US, and highlights supply chain diversification into India.
  > - **Scene 5: Sustainability Horizon & Net-Zero Economics:** Demonstrates how electric vehicles deliver a 42% lower 5-year Total Cost of Ownership compared to gas-powered vehicles."

---

### Scene 6: Performance Testing & Rubric Verification (07:15 – 08:30)
* **[Screen:]** Navigate to `/performance` and click 'Run Live Benchmarks'.
* **[Speaker Audio:]**
  > "To validate our architecture against the project rubric, we built a dedicated Performance Testing Center verifying all four required criteria:
  > 
  > 1. **Amount of Data Rendered to DB:** All 6,803 records are verified in the database with a lightweight 1.8 MB storage footprint and full table scans running in under 1 millisecond.
  > 2. **Utilization of Data Filters:** Multi-condition queries execute in 1.5 to 3.8 milliseconds thanks to composite B-Tree indexes.
  > 3. **Calculation Fields:** We cataloged and tested 12 engineered calculated fields, including Price-to-Range ratio, Fast Charge Speed, 5-Year TCO, and Level of Detail (LOD) market share expressions.
  > 4. **Unique Visualizations:** We delivered 10 distinct visualization archetypes with full mobile responsiveness."

---

### Scene 7: Tableau Embed & Flask Architecture (08:30 – 09:30)
* **[Screen:]** Navigate to `/tableau-embed`. Show desktop and tablet view toggles.
* **[Speaker Audio:]**
  > "On our Tableau Embed page, we demonstrate how this platform connects directly to Tableau Server or Tableau Public via the Tableau JavaScript Embedding API v3. 
  > 
  > Users can paste their live Tableau workbook URL directly, toggle between desktop and tablet viewport modes, and leverage full bidirectional filter synchronization with our Flask backend."

---

### Scene 8: Conclusion & Strategic Takeaways (09:30 – 10:00)
* **[Screen:]** Concluding summary slide or camera view.
* **[Speaker Audio:]**
  > "In summary, our Global Electric Vehicle Analytics Platform delivers a complete, enterprise-grade solution. From raw data collection and database normalization, to advanced SQL operations, responsive dashboards, and executive storytelling, this project equips Emily, David, and Dr. Sarah with the data-driven insights they need to accelerate the global transition toward sustainable mobility.
  > 
  > Thank you for watching!"

---
*End of Video Script*
