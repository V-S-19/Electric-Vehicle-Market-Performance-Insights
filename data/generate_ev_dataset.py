"""
EV Market Analytics Dataset Generator
Generates realistic, industry-accurate EV data for multi-year analysis (2019-2025)
Covering all vehicle categories, battery chemistries, global manufacturers, and sustainability metrics.
"""

import os
import random
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

MANUFACTURERS_DATA = {
    "Tesla": {
        "origin": "United States",
        "models": {
            "Model 3": ("Sedan", ["NCA", "LFP", "NMC"]),
            "Model Y": ("SUV", ["NMC", "LFP", "NCA"]),
            "Model S": ("Sedan", ["NCA", "NMC"]),
            "Model X": ("SUV", ["NCA", "NMC"]),
            "Cybertruck": ("Truck", ["NMC", "Solid-State"]),
            "Semi": ("Truck", ["NMC", "LFP"])
        },
        "brand_tier": "Premium",
        "primary_plants": ["United States", "China", "Germany"]
    },
    "BYD": {
        "origin": "China",
        "models": {
            "Seal": ("Sedan", ["LFP", "Sodium-Ion"]),
            "Dolphin": ("Hatchback", ["LFP", "Sodium-Ion"]),
            "Atto 3": ("SUV", ["LFP"]),
            "Han": ("Sedan", ["LFP", "NMC"]),
            "Tang": ("SUV", ["LFP", "NMC"]),
            "K9 Electric Bus": ("Electric Bus", ["LFP"]),
            "Yangwang U8": ("SUV", ["LFP", "Solid-State"])
        },
        "brand_tier": "Mass/Value",
        "primary_plants": ["China", "India"]
    },
    "Volkswagen Group": {
        "origin": "Germany",
        "models": {
            "ID.3": ("Hatchback", ["NMC", "LFP"]),
            "ID.4": ("SUV", ["NMC"]),
            "ID.5": ("SUV", ["NMC"]),
            "ID.7": ("Sedan", ["NMC"]),
            "ID.Buzz": ("Electric Bus", ["NMC"]),
            "e-Crafter": ("Truck", ["NMC"])
        },
        "brand_tier": "Mass/Premium",
        "primary_plants": ["Germany", "China", "United States", "Mexico"]
    },
    "Hyundai-Kia": {
        "origin": "South Korea",
        "models": {
            "Ioniq 5": ("SUV", ["NMC"]),
            "Ioniq 6": ("Sedan", ["NMC"]),
            "EV6": ("SUV", ["NMC"]),
            "EV9": ("SUV", ["NMC"]),
            "Kona Electric": ("SUV", ["NMC", "LFP"]),
            "Elec City Bus": ("Electric Bus", ["NMC", "LFP"])
        },
        "brand_tier": "Mass/Value",
        "primary_plants": ["South Korea", "United States", "India"]
    },
    "BMW Group": {
        "origin": "Germany",
        "models": {
            "i4": ("Sedan", ["NMC"]),
            "iX3": ("SUV", ["NMC"]),
            "iX": ("SUV", ["NMC", "Solid-State"]),
            "i7": ("Sedan", ["NMC"]),
            "CE 04": ("Two-Wheeler", ["NMC"])
        },
        "brand_tier": "Luxury",
        "primary_plants": ["Germany", "China", "United States"]
    },
    "Rivian": {
        "origin": "United States",
        "models": {
            "R1T": ("Truck", ["NMC", "LFP"]),
            "R1S": ("SUV", ["NMC", "LFP"]),
            "EDV Van": ("Truck", ["LFP", "NMC"])
        },
        "brand_tier": "Premium",
        "primary_plants": ["United States"]
    },
    "NIO": {
        "origin": "China",
        "models": {
            "ET5": ("Sedan", ["NMC", "LFP", "Solid-State"]),
            "ET7": ("Sedan", ["NMC", "Solid-State"]),
            "ES6": ("SUV", ["NMC"]),
            "ES8": ("SUV", ["NMC", "Solid-State"])
        },
        "brand_tier": "Luxury",
        "primary_plants": ["China"]
    },
    "Volvo Cars": {
        "origin": "Sweden",
        "models": {
            "EX30": ("SUV", ["LFP", "NMC"]),
            "XC40 Recharge": ("SUV", ["NMC"]),
            "EX90": ("SUV", ["NMC"]),
            "7900 Electric Bus": ("Electric Bus", ["LFP", "NMC"])
        },
        "brand_tier": "Premium",
        "primary_plants": ["Sweden", "China", "United States"]
    },
    "Tata Motors": {
        "origin": "India",
        "models": {
            "Nexon EV": ("SUV", ["LFP"]),
            "Tiago EV": ("Hatchback", ["LFP"]),
            "Punch EV": ("SUV", ["LFP"]),
            "Starbus EV": ("Electric Bus", ["LFP"]),
            "Ace EV": ("Truck", ["LFP"])
        },
        "brand_tier": "Value",
        "primary_plants": ["India"]
    },
    "Proterra": {
        "origin": "United States",
        "models": {
            "ZX5 Electric Bus": ("Electric Bus", ["NMC", "LFP"]),
            "Catalyst E2": ("Electric Bus", ["NMC"])
        },
        "brand_tier": "Commercial",
        "primary_plants": ["United States"]
    },
    "Ola Electric": {
        "origin": "India",
        "models": {
            "S1 Pro": ("Two-Wheeler", ["NMC", "LFP", "Sodium-Ion"]),
            "S1 Air": ("Two-Wheeler", ["LFP"]),
            "S1 X": ("Two-Wheeler", ["LFP", "Sodium-Ion"])
        },
        "brand_tier": "Value",
        "primary_plants": ["India"]
    },
    "SAIC Motor / MG": {
        "origin": "China",
        "models": {
            "MG4 EV": ("Hatchback", ["LFP", "NMC"]),
            "ZS EV": ("SUV", ["LFP", "NMC"]),
            "Cyberster": ("Sedan", ["NMC"])
        },
        "brand_tier": "Mass/Value",
        "primary_plants": ["China", "India"]
    }
}

REGIONS = ["Asia-Pacific", "North America", "Europe", "Latin America", "Middle East & Africa"]

REGIONAL_WEIGHTS = {
    "Asia-Pacific": 0.52,
    "Europe": 0.26,
    "North America": 0.16,
    "Latin America": 0.03,
    "Middle East & Africa": 0.03
}

YEAR_SALES_MULTIPLIER = {
    2019: 0.35,
    2020: 0.45,
    2021: 0.70,
    2022: 1.05,
    2023: 1.45,
    2024: 1.85,
    2025: 2.30
}

CATEGORY_SPECS = {
    "Two-Wheeler": {
        "battery_range": (2.5, 4.5),
        "range_km": (85, 180),
        "consumption": (3.0, 5.0),
        "price_usd": (1400, 3800),
        "maintenance_usd": (80, 220),
        "fast_charge_min": (40, 75),
        "base_annual_sales": (15000, 65000)
    },
    "Hatchback": {
        "battery_range": (32.0, 60.0),
        "range_km": (240, 440),
        "consumption": (13.5, 17.0),
        "price_usd": (18000, 36000),
        "maintenance_usd": (220, 500),
        "fast_charge_min": (25, 45),
        "base_annual_sales": (12000, 55000)
    },
    "Sedan": {
        "battery_range": (55.0, 95.0),
        "range_km": (400, 690),
        "consumption": (14.0, 18.5),
        "price_usd": (32000, 95000),
        "maintenance_usd": (350, 850),
        "fast_charge_min": (18, 35),
        "base_annual_sales": (18000, 75000)
    },
    "SUV": {
        "battery_range": (62.0, 115.0),
        "range_km": (360, 630),
        "consumption": (17.5, 24.0),
        "price_usd": (38000, 115000),
        "maintenance_usd": (400, 950),
        "fast_charge_min": (20, 40),
        "base_annual_sales": (25000, 90000)
    },
    "Truck": {
        "battery_range": (110.0, 215.0),
        "range_km": (340, 580),
        "consumption": (28.0, 44.0),
        "price_usd": (58000, 145000),
        "maintenance_usd": (600, 1400),
        "fast_charge_min": (30, 55),
        "base_annual_sales": (4000, 22000)
    },
    "Electric Bus": {
        "battery_range": (220.0, 460.0),
        "range_km": (220, 420),
        "consumption": (80.0, 125.0),
        "price_usd": (280000, 560000),
        "maintenance_usd": (1800, 4200),
        "fast_charge_min": (45, 90),
        "base_annual_sales": (800, 4500)
    }
}

BATTERY_TECH_SPECS = {
    "LFP": {
        "lifespan_cycles": (2800, 4200),
        "density_wh_kg": (160, 200),
        "cost_modifier": 0.82,
        "charge_multiplier": 1.15,
        "efficiency_score": 8.5
    },
    "NMC": {
        "lifespan_cycles": (1800, 2500),
        "density_wh_kg": (220, 280),
        "cost_modifier": 1.05,
        "charge_multiplier": 0.95,
        "efficiency_score": 9.0
    },
    "NCA": {
        "lifespan_cycles": (1400, 2100),
        "density_wh_kg": (250, 300),
        "cost_modifier": 1.12,
        "charge_multiplier": 0.90,
        "efficiency_score": 9.2
    },
    "Sodium-Ion": {
        "lifespan_cycles": (2200, 3200),
        "density_wh_kg": (130, 170),
        "cost_modifier": 0.68,
        "charge_multiplier": 0.85,
        "efficiency_score": 8.0
    },
    "Solid-State": {
        "lifespan_cycles": (3000, 4500),
        "density_wh_kg": (350, 450),
        "cost_modifier": 1.45,
        "charge_multiplier": 0.55,
        "efficiency_score": 9.8
    }
}

REGIONAL_INFRA_INDEX = {
    "Asia-Pacific": 78,
    "Europe": 84,
    "North America": 72,
    "Latin America": 38,
    "Middle East & Africa": 45
}

def generate_dataset(target_rows=6500):
    rows = []
    record_id = 10001
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]

    while len(rows) < target_rows:
        for year in years:
            for mfg, mfg_info in MANUFACTURERS_DATA.items():
                for model, (cat, allowed_batteries) in mfg_info["models"].items():
                    # Check tech availability by year
                    available_batteries = []
                    for b in allowed_batteries:
                        if b == "Solid-State" and year < 2024:
                            continue
                        if b == "Sodium-Ion" and year < 2023:
                            continue
                        available_batteries.append(b)

                    if not available_batteries:
                        available_batteries = ["NMC" if "NMC" in allowed_batteries else allowed_batteries[0]]

                    for region in REGIONS:
                        # Probabilistic inclusion per region
                        reg_prob = REGIONAL_WEIGHTS[region]
                        if mfg in ["Tata Motors", "Ola Electric"] and region not in ["Asia-Pacific", "Middle East & Africa", "Europe"]:
                            if random.random() > 0.08:
                                continue
                        elif mfg in ["Rivian", "Proterra"] and region not in ["North America", "Europe"]:
                            if random.random() > 0.12:
                                continue
                        elif random.random() > (reg_prob * 1.5):
                            continue

                        b_tech = random.choice(available_batteries)
                        cat_cfg = CATEGORY_SPECS[cat]
                        bat_cfg = BATTERY_TECH_SPECS[b_tech]

                        # Specs calculation
                        b_cap = round(random.uniform(*cat_cfg["battery_range"]) * (1.0 + (year - 2019) * 0.03), 1)
                        
                        # Energy consumption improves over time
                        energy_eff = round(random.uniform(*cat_cfg["consumption"]) * (1.0 - (year - 2019) * 0.02), 2)
                        
                        # Driving range calculated from capacity and efficiency
                        calculated_range = int((b_cap / energy_eff) * 100 * random.uniform(0.92, 1.08))
                        driving_range = max(cat_cfg["range_km"][0], min(cat_cfg["range_km"][1] * 1.3, calculated_range))

                        # Fast charging time
                        fast_charge = int(random.uniform(*cat_cfg["fast_charge_min"]) * bat_cfg["charge_multiplier"] * (1.0 - (year - 2019) * 0.04))
                        fast_charge = max(12, fast_charge)

                        # Life cycles
                        lifespan = int(random.uniform(*bat_cfg["lifespan_cycles"]) + (year - 2019) * 50)

                        # Base price
                        price_mult = bat_cfg["cost_modifier"] * (0.96 ** (year - 2019))
                        base_price = int(random.uniform(*cat_cfg["price_usd"]) * price_mult)

                        # Manufacturing Country
                        mfg_country = random.choice(mfg_info["primary_plants"])

                        # Sales units
                        base_sales = random.uniform(*cat_cfg["base_annual_sales"])
                        brand_weight = 1.6 if mfg in ["Tesla", "BYD"] else (1.2 if mfg in ["Volkswagen Group", "Hyundai-Kia"] else 0.85)
                        tech_weight = 1.15 if b_tech in ["LFP", "NMC"] else (1.25 if b_tech == "Solid-State" else 0.95)
                        
                        annual_sales = int(base_sales * brand_weight * tech_weight * REGIONAL_WEIGHTS[region] * YEAR_SALES_MULTIPLIER[year] * random.uniform(0.80, 1.25))
                        annual_sales = max(15, annual_sales)

                        # Revenue
                        revenue = annual_sales * base_price

                        # Customer rating & satisfaction
                        rating_base = 4.1 if mfg_info["brand_tier"] in ["Luxury", "Premium"] else 3.8
                        customer_rating = round(min(5.0, max(3.0, rating_base + random.uniform(-0.4, 0.7) + (year - 2019) * 0.04)), 2)
                        satisfaction_score = round(min(98.5, max(68.0, (customer_rating / 5.0) * 100 + random.uniform(-3, 3))), 1)

                        # Maintenance cost
                        maint_cost = int(random.uniform(*cat_cfg["maintenance_usd"]) * (0.97 ** (year - 2019)))

                        # Sustainability: Tons of CO2 saved
                        # Avg ICE car emits ~2.3 kg CO2 per liter, ~7.5L/100km = 172.5g CO2/km
                        # EV emits based on regional grid ~45g-90g CO2/km
                        # Net savings ~100g CO2/km. Avg 15,000 km/year = 1.5 tons CO2 saved per vehicle per year.
                        # Buses and trucks save 10-25x more!
                        co2_factor = 28.0 if cat == "Electric Bus" else (14.0 if cat == "Truck" else (0.5 if cat == "Two-Wheeler" else 1.8))
                        co2_saved_tons = round(annual_sales * co2_factor, 1)

                        # Regional Charging Infrastructure Index
                        infra_index = REGIONAL_INFRA_INDEX[region] + int((year - 2019) * 2.2)
                        infra_index = min(98, infra_index)

                        # Safety & Warranty
                        safety_stars = random.choice([4, 5]) if cat in ["Sedan", "SUV"] and mfg_info["brand_tier"] != "Value" else random.choice([3, 4, 5])
                        warranty_years = random.choice([6, 8, 8, 10])

                        rows.append({
                            "Record_ID": record_id,
                            "Vehicle_ID": f"EV-{mfg[:3].upper()}-{year}-{record_id % 10000:04d}",
                            "Manufacturer": mfg,
                            "Model_Name": model,
                            "Vehicle_Category": cat,
                            "Model_Year": year,
                            "Battery_Technology": b_tech,
                            "Battery_Capacity_kWh": b_cap,
                            "Driving_Range_km": driving_range,
                            "Energy_Consumption_kWh_100km": energy_eff,
                            "Fast_Charging_Time_min": fast_charge,
                            "Battery_Life_Cycles": lifespan,
                            "Base_Price_USD": base_price,
                            "Annual_Sales_Units": annual_sales,
                            "Total_Revenue_USD": revenue,
                            "Manufacturing_Country": mfg_country,
                            "Sales_Region": region,
                            "Customer_Rating": customer_rating,
                            "Customer_Satisfaction_Score_pct": satisfaction_score,
                            "Annual_Maintenance_Cost_USD": maint_cost,
                            "Carbon_Emissions_Saved_Tons": co2_saved_tons,
                            "Charging_Infrastructure_Index": infra_index,
                            "Safety_Rating_Stars": safety_stars,
                            "Warranty_Years": warranty_years
                        })
                        record_id += 1
                        if len(rows) >= target_rows:
                            break
                    if len(rows) >= target_rows:
                        break
                if len(rows) >= target_rows:
                    break

    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(current_dir, "ev_market_data.csv")
    print("Generating comprehensive EV Market dataset...")
    df = generate_dataset(target_rows=6800)
    df.to_csv(output_csv, index=False)
    print(f"Successfully generated {len(df)} records!")
    print(f"Saved to: {output_csv}")
    print("\nDataset Summary Preview:")
    print(df.info())
    print("\nSample records:")
    print(df.head(3))
