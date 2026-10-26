# In-Depth Problem Definition & Persona Strategy Framework
## Global Electric Vehicle (EV) Industry Analytics

---

## 1. Industry Context & Strategic Inflection Point

The global automotive landscape is witnessing the most profound technological transition since the assembly line: the migration from internal combustion engines (ICE) to electric powertrains. This transition is characterized by three simultaneous macro-forces:

1. **Regulatory and Decarbonization Mandates:** Sovereign net-zero commitments (e.g., Paris Agreement, European Union's 2035 ban on new ICE vehicle sales, US Inflation Reduction Act incentives, China New Energy Vehicle targets) are establishing firm statutory horizons for full fleet electrification.
2. **Technological Convergence:** Rapid advancements in battery cell chemistry—specifically the cost deflation of Lithium Iron Phosphate (LFP), the energy density optimizations of Nickel Manganese Cobalt (NMC), and the emergence of Sodium-Ion and Solid-State architectures—have pushed electric vehicles past the total cost of ownership (TCO) parity threshold.
3. **Multi-Segment Market Expansion:** EV availability has broadened beyond early-adopter luxury sedans to encompass high-volume hatchbacks, family SUVs, long-haul commercial trucks, city transit buses, and high-frequency urban two-wheelers.

---

## 2. Deep-Dive Persona Analysis & KPI Matrix

To ensure analytical precision, the problem is formulated through the strategic lenses of three key industry stakeholders:

```
+-------------------------------------------------------------------------------------------------+
|                                 GLOBAL EV ANALYTICS STAKEHOLDERS                                |
+---------------------------------+-------------------------------+-------------------------------+
|   Emily Johnson                 |   David Chen                  |   Dr. Sarah Williams          |
|   Market Strategy Director      |   Automotive BI Manager       |   Sustainable Mobility Analyst|
|   (Global Automaker)            |   (Consulting Firm)           |   (Clean Energy Institute)    |
+---------------------------------+-------------------------------+-------------------------------+
| Focus:                          | Focus:                        | Focus:                        |
| - Category revenue share        | - Competitive market share    | - Chemistry efficiency        |
| - Satisfaction vs range         | - Brand tier positioning      | - Lifecycle durability        |
| - High-growth segments          | - Manufacturing geography     | - Carbon abatement ROI        |
+---------------------------------+-------------------------------+-------------------------------+
```

---

### Persona 1: Emily Johnson — EV Market Strategy Director

#### 1. Background & Scope
Emily directs global product planning and market entry strategy for a major automotive OEM. Her mission is to allocate capital expenditures toward vehicle platforms and battery chemistries that maximize operating profits while satisfying consumer range expectations.

#### 2. Strategic Objectives
* Identify which vehicle categories (Hatchback, Sedan, SUV, Bus, Truck, Two-Wheeler) deliver maximum revenue and unit volume.
* Quantify the inflection point where additional driving range (km) ceases to produce meaningful gains in customer satisfaction.
* Evaluate the commercial viability of substituting expensive NMC battery packs with cost-effective LFP or Sodium-Ion packs in entry-level vehicle lines.

#### 3. Core KPI Framework
| KPI Name | Formula | Strategic Significance |
| :--- | :--- | :--- |
| **Category Revenue Share (%)** | `(Category Revenue / Total Revenue) * 100` | Sizing platform capital allocation. |
| **Price per Range km ($/km)** | `Base Price USD / Driving Range km` | Consumer value proposition benchmark. |
| **Satisfaction Elasticity** | `Δ Satisfaction % / Δ Driving Range km` | Identifying the point of diminishing range returns. |
| **Platform 5-Year CAGR (%)** | `((Sales 2025 / Sales 2019)^(1/6) - 1) * 100` | Prioritizing long-term growth segments. |

---

### Persona 2: David Chen — Automotive Business Intelligence Manager

#### 1. Background & Scope
David leads market intelligence for an international management consultancy. His mandate is to advise automotive executive boards and sovereign investment funds on competitive positioning, supply chain exposure, and market penetration strategies.

#### 2. Strategic Objectives
* Benchmark the annual sales trajectories and global market shares of leading pure-play EV pioneers versus legacy automotive conglomerates.
* Map geographical production centers (manufacturing countries) against major consumption markets (sales regions) to detect supply chain vulnerabilities.
* Track battery technology sourcing across tier-1 manufacturers to evaluate supply chain diversification.

#### 3. Core KPI Framework
| KPI Name | Formula | Strategic Significance |
| :--- | :--- | :--- |
| **Global Market Share (%)** | `(Mfg Sales / Total Global Sales) * 100` | Competitive rank and pricing power. |
| **Export Dependency Ratio (%)** | `(Exported Units / Total Manufactured Units) * 100` | Exposure to cross-border tariff risks. |
| **LFP Adoption Rate (%)** | `(LFP Units / Total Mfg Units) * 100` | Cost structure competitiveness. |
| **Price Dispersion Index** | `StdDev(Base Price) across Portfolio` | Breadth of brand portfolio coverage. |

---

### Persona 3: Dr. Sarah Williams — Sustainable Mobility Research Analyst

#### 1. Background & Scope
Dr. Williams is a senior researcher at a multilateral clean energy think tank. Her objective is to provide empirical, data-driven policy recommendations to transport ministries and climate task forces on vehicle efficiency, battery durability, and carbon emissions reduction.

#### 2. Strategic Objectives
* Conduct comprehensive techno-economic benchmarking across five battery chemistries (LFP, NMC, NCA, Sodium-Ion, Solid-State) regarding energy consumption (kWh/100km), fast-charge time, and cycle life.
* Evaluate fleet-level carbon abatement to quantify the emissions displacement of passenger cars versus commercial electric transit buses.
* Document historical progress from 2019 to 2025 in vehicle range and charging turnaround speed.

#### 3. Core KPI Framework
| KPI Name | Formula | Strategic Significance |
| :--- | :--- | :--- |
| **Energy Consumption (kWh/100km)** | `Avg(Energy Consumption)` | Powertrain and battery pack efficiency. |
| **Fast Charge Turnaround (km/min)** | `Driving Range km / Fast Charge Mins` | Infrastructure throughput efficiency. |
| **Annual Carbon Abatement (Tons)** | `Sum(Carbon Emissions Saved Tons)` | Environmental impact and climate policy compliance. |
| **Abatement ROI (kg CO2 / $)** | `(Carbon Saved kg) / Acquisition Price USD` | Optimizing public municipal subsidies. |

---

## 3. Methodological Workflow & Expected Business Impact

1. **Unified Enterprise Data Foundation:** By harmonizing 6,803 records into SQLite and Tableau, all three personas access a single source of truth.
2. **Actionable Executive Dashboards:** Interactive filtering enables cross-functional discovery (e.g., Emily discovering that SUV buyer satisfaction peaks at 520 km, David spotting BYD's LFP dominance, and Sarah proving the 15x carbon leverage of electric buses).
3. **Tableau Story Narrative:** Contextualizes findings into five coherent chapters suitable for boardroom presentations.
