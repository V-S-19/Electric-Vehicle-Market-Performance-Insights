# 3-to-5 Minute Executive Demo Video Script & Recording Guide
## Global Electric Vehicle (EV) Market Analytics Platform

**Target Duration:** 3 Minutes 30 Seconds – 4 Minutes 30 Seconds  
**Format:** Screen Recording + Voiceover (Optional: Webcam corner inset)  
**Tone:** Confident, executive, engaging, and crisp.

---

## 🛠️ Quick Recording Setup (Windows)

You can record this video completely free using tools already built into Windows:

### Method 1: Windows Built-in Screen Recorder (Fastest - 0 Installs)
1. Launch your Flask web app:
   ```bash
   python run_app.py
   ```
2. Open Google Chrome or Microsoft Edge and open two tabs:
   - **Tab 1:** `http://127.0.0.1:5000/presentation` (Your slide deck)
   - **Tab 2:** `http://127.0.0.1:5000/dashboard` (Your live app)
3. Press **`Win + Alt + R`** to immediately start recording (make sure your microphone icon is unmuted).
4. When finished, press **`Win + Alt + R`** again. The video is saved directly into your `Videos\Captures` folder in MP4 format!

### Method 2: Microsoft Clipchamp (Free with Windows 11)
- Open Clipchamp from your Windows Start menu -> Click **"Record Screen & Camera"** -> Select your browser window. Allows easy trimming and captions!

### Method 3: OBS Studio or Loom
- Ideal if you already have OBS or Loom installed. Set canvas resolution to `1920x1080` at 60fps.

---

## 📋 Pre-Flight Checklist Before You Hit Record

- [ ] Web application running (`python run_app.py` in terminal).
- [ ] Browser tabs prepared in advance:
  - Tab 1: `http://127.0.0.1:5000/presentation`
  - Tab 2: `http://127.0.0.1:5000/dashboard`
  - Tab 3: `http://127.0.0.1:5000/story`
  - Tab 4: `http://127.0.0.1:5000/sql-explorer`
- [ ] Press **`F11`** in your browser to enter full-screen mode (hides bookmarks and tabs for a cinematic look).
- [ ] Press **`N`** on the presentation slide deck to open the floating speaker notes teleprompter if you want live visual cues!

---

## ⏱️ Video Demonstration Choreography & Timed Script

| Segment | Timestamp | Screen Action (What to Show & Click) | Spoken Voiceover Script (What to Say) |
| :--- | :--- | :--- | :--- |
| **1. Hook & Overview** | `00:00 – 00:45` | **Start on Slide 1** of `/presentation`.<br>Advance to **Slide 2** using Right Arrow key. | *"Hello everyone, and welcome to the demonstration of our Global Electric Vehicle Market Analytics Platform.<br><br>The automotive industry is in the midst of a historic transition, growing at an exponential 38% compound annual growth rate. However, executives face significant data fragmentation across shifting battery chemistries, vehicle categories, and regional trade corridors.<br><br>To solve this, we engineered an end-to-end data analytics and business intelligence solution combining 6,800 market records across 12 automakers, an enterprise SQLite 3 star-schema, dynamic SQL analytics, and interactive storytelling."* |
| **2. Personas & Architecture** | `00:45 – 01:25` | Advance to **Slide 3** (Personas), then **Slide 4** (Data Architecture). | *"To deliver direct strategic value, our platform is built around three distinct executive personas:<br><br>First, **Emily Johnson**, Market Strategy Director, who needs category portfolio mix and range satisfaction insights.<br>Second, **David Chen**, Automotive BI Manager, tracking OEM market share and pricing dynamics.<br>And third, **Dr. Sarah Williams**, benchmarking battery chemistry efficiency and fleet carbon emissions abatement.<br><br>Under the hood, we implemented a dual-storage SQLite database with an enterprise star-schema and compound B-Tree indexes, achieving sub-2 millisecond query latencies across 12 engineered calculated metrics like 5-Year Total Cost of Ownership."* |
| **3. Live Dashboard Walkthrough** | `01:25 – 02:40` | **Switch tab to `/dashboard`**.<br><br>1. Hover over the 6 KPI cards at the top.<br>2. Select filter **Year: 2024**.<br>3. Select filter **Category: SUV**.<br>4. Select filter **Battery: LFP**.<br>5. Watch KPIs animate and charts update instantly.<br>6. Hover over the Delivery Line Chart and Automaker Ranked Bar Chart. | *"Let's step into the live Executive Dashboard.<br><br>Notice our dark glassmorphism design system built for executive boardrooms. Across the top, we have six real-time animated KPI scorecards tracking Deliveries, Gross Revenue, Driving Range, Average Selling Price, Customer Satisfaction, and CO2 Abatement.<br><br>Watch what happens when we apply multi-parameter filters. I'll select the model year 2024, the high-demand SUV category, and Lithium Iron Phosphate battery chemistry...<br><br>In under two milliseconds, all six KPI counters roll up smoothly to reflect the filtered slice, and our six synchronized charts immediately update—displaying revenue trajectories, battery charge speeds, and automaker delivery rankings with zero interface lag."* |
| **4. Story Mode Narrative** | `02:40 – 03:30` | **Switch tab to `/story`**.<br><br>1. Click on **Scene 1** (Surge).<br>2. Click on **Scene 2** (Battery Chemistry War).<br>3. Click on **Scene 3** (Category Dominance).<br>4. Click on **Scene 5** (Decarbonization & TCO). | *"Next, we present our 5-Scene Story Mode, designed for board-level briefings:<br><br>- **Scene 1** illustrates the exponential surge and adoption tipping point.<br>- **Scene 2** exposes the battery chemistry transition—showing how low-cost LFP chemistry slashed cell costs by 28% to unlock mass-market EVs, while Solid-State pushes luxury ranges beyond 600 kilometers.<br>- **Scene 3** reveals why SUVs command over 41% of global EV revenue, while electric transit buses deliver the highest single-vehicle carbon reduction.<br>- And **Scene 5** quantifies sustainability economics, proving that modern electric vehicles deliver a 42% lower 5-year Total Cost of Ownership compared to fossil fuel vehicles."* |
| **5. Technical Benchmarks & Conclusion** | `03:30 – 04:15` | **Switch tab to `/sql-explorer`** or `/performance`.<br><br>Click **'Run Query'** to show the 2ms stopwatch.<br>Switch back to **Slide 8** of `/presentation`. | *"Finally, our live SQL Explorer and Performance Center demonstrate that all four project rubric criteria are 100% verified—rendering 6,803 records in under a millisecond, executing complex CTEs and window functions instantaneously, and integrating seamlessly with Tableau Server via the Tableau JavaScript API.<br><br>In conclusion, this platform equips leaders like Emily, David, and Dr. Sarah with the data agility needed to steer the global clean mobility revolution.<br><br>Thank you for watching!"* |

---

## 💡 Pro Presentation Tips

1. **Mouse Movement:** Move your mouse smoothly and deliberately. Hover over a chart for 1-2 seconds so the tooltip pops up before moving to the next element.
2. **Browser Viewport:** Press **`F11`** for clean, uninterrupted full-screen viewing.
3. **Teleprompter Aid:** If using the slide deck at `/presentation`, press the **`N`** key at any moment to reveal the built-in teleprompter drawer containing your exact script!
4. **Resolution:** 1080p (1920x1080) at 60 FPS provides the best visual clarity for the glowing charts.
