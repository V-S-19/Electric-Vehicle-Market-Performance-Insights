/**
 * Main Application Controller for EV Market Analytics
 * Manages Filters, KPI Counter animations, Story Scenes, SQL Explorer, and Performance Benchmarks.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Check which page is currently loaded
  if (document.getElementById('filterYear')) {
    initDashboardPage();
  }
  if (document.getElementById('storySceneContainer')) {
    initStoryPage();
  }
  if (document.getElementById('sqlQueryInput')) {
    initSqlExplorerPage();
  }
  if (document.getElementById('runPerformanceBtn')) {
    initPerformancePage();
  }
});

// ----------------------------------------------------------------------------
// DASHBOARD CONTROLLER
// ----------------------------------------------------------------------------
function initDashboardPage() {
  const filterYear = document.getElementById('filterYear');
  const filterCategory = document.getElementById('filterCategory');
  const filterBattery = document.getElementById('filterBattery');
  const filterRegion = document.getElementById('filterRegion');
  const filterManufacturer = document.getElementById('filterManufacturer');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');

  // Load filter options from API
  fetch('/api/filter-options')
    .then(r => r.json())
    .then(data => {
      populateSelect(filterYear, data.years);
      populateSelect(filterCategory, data.categories);
      populateSelect(filterBattery, data.batteries);
      populateSelect(filterRegion, data.regions);
      populateSelect(filterManufacturer, data.manufacturers);
      // Fetch initial data
      updateDashboardData();
    })
    .catch(err => console.error("Filter options loading failed:", err));

  // Attach change listeners
  [filterYear, filterCategory, filterBattery, filterRegion, filterManufacturer].forEach(el => {
    if (el) el.addEventListener('change', () => updateDashboardData());
  });

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener('click', () => {
      filterYear.value = 'all';
      filterCategory.value = 'all';
      filterBattery.value = 'all';
      filterRegion.value = 'all';
      filterManufacturer.value = 'all';
      updateDashboardData();
    });
  }
}

function populateSelect(selectEl, items) {
  if (!selectEl || !items) return;
  items.forEach(item => {
    const opt = document.createElement('option');
    opt.value = item;
    opt.textContent = item;
    selectEl.appendChild(opt);
  });
}

function updateDashboardData() {
  const year = document.getElementById('filterYear')?.value || 'all';
  const category = document.getElementById('filterCategory')?.value || 'all';
  const battery = document.getElementById('filterBattery')?.value || 'all';
  const region = document.getElementById('filterRegion')?.value || 'all';
  const manufacturer = document.getElementById('filterManufacturer')?.value || 'all';

  const params = new URLSearchParams({ year, category, battery, region, manufacturer });
  const latencyBadge = document.getElementById('queryLatencyBadge');
  if (latencyBadge) latencyBadge.textContent = 'Querying...';

  fetch(`/api/data?${params.toString()}`)
    .then(r => r.json())
    .then(res => {
      if (latencyBadge) {
        latencyBadge.textContent = `⚡ ${res.execution_time_ms} ms (${res.record_count.toLocaleString()} rows)`;
      }

      // Update KPIs
      animateCounter('kpiSalesUnits', res.kpis.total_sales_units, false);
      animateRevenue('kpiRevenue', res.kpis.total_revenue_usd);
      animateCounter('kpiAvgRange', res.kpis.avg_driving_range_km, false, ' km');
      animateCounter('kpiAvgPrice', res.kpis.avg_base_price_usd, true, '');
      animateCounter('kpiAvgSatisfaction', res.kpis.avg_satisfaction_pct, false, '%');
      animateCounter('kpiCo2Saved', Math.round(res.kpis.total_co2_saved_tons / 1000), false, 'k Tons');

      // Update Charts
      const ctxYearly = document.getElementById('chartYearly');
      if (ctxYearly && res.charts.yearly) EVCharts.initYearlyChart(ctxYearly, res.charts.yearly);

      const ctxCategory = document.getElementById('chartCategory');
      if (ctxCategory && res.charts.category) EVCharts.initCategoryDonut(ctxCategory, res.charts.category);

      const ctxMfg = document.getElementById('chartMfg');
      if (ctxMfg && res.charts.manufacturer) EVCharts.initManufacturerBar(ctxMfg, res.charts.manufacturer);

      const ctxBattery = document.getElementById('chartBattery');
      if (ctxBattery && res.charts.battery) EVCharts.initBatteryRadar(ctxBattery, res.charts.battery);

      const ctxRegion = document.getElementById('chartRegion');
      if (ctxRegion && res.charts.region) EVCharts.initRegionBar(ctxRegion, res.charts.region);

      const ctxRangePrice = document.getElementById('chartRangePrice');
      if (ctxRangePrice && res.charts.cat_range_price) EVCharts.initRangePriceScatter(ctxRangePrice, res.charts.cat_range_price);
    })
    .catch(err => console.error("Error fetching filtered data:", err));
}

function animateCounter(id, targetVal, isCurrency = false, suffix = '') {
  const el = document.getElementById(id);
  if (!el || targetVal === undefined) return;
  const startVal = 0;
  const duration = 600;
  const startTime = performance.now();

  function updateNumber(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const currentVal = Math.floor(progress * targetVal);
    const prefix = isCurrency ? '$' : '';
    el.textContent = `${prefix}${currentVal.toLocaleString()}${suffix}`;
    if (progress < 1) requestAnimationFrame(updateNumber);
  }
  requestAnimationFrame(updateNumber);
}

function animateRevenue(id, revenueUsd) {
  const el = document.getElementById(id);
  if (!el || revenueUsd === undefined) return;
  const inBillions = (revenueUsd / 1e9).toFixed(2);
  el.textContent = `$${inBillions}B`;
}

// ----------------------------------------------------------------------------
// STORY CONTROLLER (Tableau Multi-Scene Narrative)
// ----------------------------------------------------------------------------
const STORY_SCENES = [
  {
    id: 1,
    title: "Scene 1: The Exponential Surge — Market Takeoff (2019-2025)",
    badge: "Market Growth",
    narrative: "Between 2019 and 2025, global electric vehicle adoption surged exponentially. Driven by strict emissions mandates in the EU, China's aggressive New Energy Vehicle subsidies, and rapid US market penetration, sales volumes expanded more than sixfold. This explosive growth signaled the transition of EVs from niche early-adopter novelties into mainstream automotive volume leaders.",
    takeaway: "Key Strategic Takeaway: Annual global sales volumes grew at over 38% CAGR. Sedans and SUVs alone captured over 65% of all EV revenue by 2025.",
    chartType: "yearly",
    filterPayload: { year: "all" }
  },
  {
    id: 2,
    title: "Scene 2: Battery Chemistry War — LFP vs NMC vs Solid-State",
    badge: "Technology Evolution",
    narrative: "Battery chemistry is the battleground of competitive differentiation. Lithium Iron Phosphate (LFP) emerged as the volume king for mass-market cars and commercial buses due to its extraordinary lifespan (>3,500 cycles) and thermal stability without cobalt. Meanwhile, High-Nickel NMC continues to dominate high-performance SUVs, while next-generation Solid-State prototypes (entering in 2024-2025) demonstrate under-15-minute ultra-fast charging and 600+ km ranges.",
    takeaway: "Key Strategic Takeaway: LFP accounts for over 52% of commercial vehicle deliveries and 40% of mass-market hatchbacks, slashing cell costs by 28%.",
    chartType: "battery",
    filterPayload: { year: "all" }
  },
  {
    id: 3,
    title: "Scene 3: Category Dominance — The Rise of the Electric SUV & Fleet Bus",
    badge: "Segment Analysis",
    narrative: "Consumers globally overwhelmingly prefer SUVs, leading to record sales across models like the Tesla Model Y, BYD Song/Tang, and VW ID.4. Concurrently, municipal governments have spearheaded the electrification of public transit, making Electric Buses the single largest per-vehicle carbon reduction category in urban centers.",
    takeaway: "Key Strategic Takeaway: SUVs generate the highest profit margins ($12,000+ per unit gross margin), while Electric Buses abate up to 28 tons of CO2 annually per vehicle.",
    chartType: "category",
    filterPayload: { year: "all" }
  },
  {
    id: 4,
    title: "Scene 4: Global Manufacturing Superpowers & Supply Chains",
    badge: "Geographical Distribution",
    narrative: "China continues to serve as the dominant manufacturing powerhouse for global EV production, leveraging its integrated battery supply chain. However, major localized assembly hubs in Germany, the United States, and emerging hubs in India have witnessed substantial capacity expansions to satisfy domestic consumer demand and hedge against geopolitical supply disruptions.",
    takeaway: "Key Strategic Takeaway: Over 55% of all battery cells and vehicle assemblies originate in the Asia-Pacific region, with European plants accelerating localize-for-local manufacturing.",
    chartType: "region",
    filterPayload: { year: "all" }
  },
  {
    id: 5,
    title: "Scene 5: Sustainability Horizon & Net-Zero Economics",
    badge: "Decarbonization",
    narrative: "Over 75,000 km of driving, the average electric vehicle delivers a 42% lower Total Cost of Ownership (TCO) compared to equivalent internal combustion engine (ICE) vehicles. Furthermore, the global EV fleet represented in this dataset has collectively abated millions of metric tons of greenhouse gas emissions, directly advancing the Paris Agreement targets.",
    takeaway: "Key Strategic Takeaway: EV operating costs average only $2.40 per 100 km vs $11.80 for gasoline, making corporate fleet electrification an undeniable economic imperative.",
    chartType: "rangePrice",
    filterPayload: { year: "all" }
  }
];

let currentSceneIndex = 0;

function initStoryPage() {
  const navContainer = document.getElementById('storyNav');
  const prevBtn = document.getElementById('storyPrevBtn');
  const nextBtn = document.getElementById('storyNextBtn');

  // Render scene buttons
  if (navContainer) {
    navContainer.innerHTML = '';
    STORY_SCENES.forEach((scene, idx) => {
      const btn = document.createElement('button');
      btn.className = `scene-btn ${idx === 0 ? 'active' : ''}`;
      btn.id = `sceneBtn_${idx}`;
      btn.innerHTML = `<span class="scene-badge">${scene.badge}</span> ${scene.title.split('—')[0]}`;
      btn.addEventListener('click', () => loadStoryScene(idx));
      navContainer.appendChild(btn);
    });
  }

  if (prevBtn) prevBtn.addEventListener('click', () => {
    if (currentSceneIndex > 0) loadStoryScene(currentSceneIndex - 1);
  });

  if (nextBtn) nextBtn.addEventListener('click', () => {
    if (currentSceneIndex < STORY_SCENES.length - 1) loadStoryScene(currentSceneIndex + 1);
  });

  loadStoryScene(0);
}

function loadStoryScene(index) {
  currentSceneIndex = index;
  const scene = STORY_SCENES[index];

  // Update navigation button active state
  document.querySelectorAll('.scene-btn').forEach((btn, idx) => {
    btn.classList.toggle('active', idx === index);
  });

  // Update narrative details
  const titleEl = document.getElementById('storySceneTitle');
  const narrativeEl = document.getElementById('storySceneNarrative');
  const takeawayEl = document.getElementById('storySceneTakeaway');
  const counterEl = document.getElementById('storySceneCounter');

  if (titleEl) titleEl.textContent = scene.title;
  if (narrativeEl) narrativeEl.textContent = scene.narrative;
  if (takeawayEl) takeawayEl.textContent = scene.takeaway;
  if (counterEl) counterEl.textContent = `Scene ${index + 1} of ${STORY_SCENES.length}`;

  // Fetch scene data and render appropriate chart
  fetch('/api/data?year=all')
    .then(r => r.json())
    .then(res => {
      const storyChartCtx = document.getElementById('storyChartCanvas');
      if (!storyChartCtx) return;

      if (scene.chartType === 'yearly') {
        EVCharts.initYearlyChart(storyChartCtx, res.charts.yearly);
      } else if (scene.chartType === 'battery') {
        EVCharts.initBatteryRadar(storyChartCtx, res.charts.battery);
      } else if (scene.chartType === 'category') {
        EVCharts.initCategoryDonut(storyChartCtx, res.charts.category);
      } else if (scene.chartType === 'region') {
        EVCharts.initRegionBar(storyChartCtx, res.charts.region);
      } else if (scene.chartType === 'rangePrice') {
        EVCharts.initRangePriceScatter(storyChartCtx, res.charts.cat_range_price);
      }
    });
}

// ----------------------------------------------------------------------------
// SQL EXPLORER CONTROLLER
// ----------------------------------------------------------------------------
function initSqlExplorerPage() {
  const queryInput = document.getElementById('sqlQueryInput');
  const executeBtn = document.getElementById('executeSqlBtn');
  const resultsDiv = document.getElementById('sqlResultsContainer');
  const latencySpan = document.getElementById('sqlExecutionLatency');
  const rowCountSpan = document.getElementById('sqlRowCount');

  // Query Preset Chips
  document.querySelectorAll('.preset-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const presetQuery = chip.getAttribute('data-query');
      if (presetQuery && queryInput) {
        queryInput.value = presetQuery.trim();
        executeSqlQuery();
      }
    });
  });

  if (executeBtn) {
    executeBtn.addEventListener('click', executeSqlQuery);
  }

  function executeSqlQuery() {
    const query = queryInput.value.trim();
    if (!query) return;

    if (resultsDiv) resultsDiv.innerHTML = '<div style="padding:2rem;text-align:center;color:#94a3b8;">Executing SQL query against SQLite database...</div>';

    fetch('/api/run-sql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query })
    })
      .then(r => r.json())
      .then(res => {
        if (res.error) {
          resultsDiv.innerHTML = `<div style="padding:1rem;color:#f43f5e;background:rgba(244,63,94,0.1);border-radius:8px;"><strong>SQL Error:</strong> ${res.error}</div>`;
          return;
        }

        if (latencySpan) latencySpan.textContent = `Latency: ${res.execution_time_ms} ms`;
        if (rowCountSpan) rowCountSpan.textContent = `Rows: ${res.total_rows}`;

        // Render Table
        let tableHtml = '<div class="table-responsive"><table class="custom-table"><thead><tr>';
        res.columns.forEach(col => {
          tableHtml += `<th>${col}</th>`;
        });
        tableHtml += '</tr></thead><tbody>';

        res.rows.forEach(row => {
          tableHtml += '<tr>';
          row.forEach(cell => {
            const displayVal = (typeof cell === 'number') ? (cell % 1 === 0 ? cell.toLocaleString() : cell.toFixed(2)) : cell;
            tableHtml += `<td>${displayVal}</td>`;
          });
          tableHtml += '</tr>';
        });

        tableHtml += '</tbody></table></div>';
        if (res.is_truncated) {
          tableHtml += '<div style="font-size:0.75rem;color:#94a3b8;margin-top:8px;">* Display limited to first 100 rows.</div>';
        }

        resultsDiv.innerHTML = tableHtml;
      })
      .catch(err => {
        resultsDiv.innerHTML = `<div style="color:#f43f5e;">Network or Server Error: ${err}</div>`;
      });
  }
}

// ----------------------------------------------------------------------------
// PERFORMANCE TESTING BENCHMARKS CONTROLLER
// ----------------------------------------------------------------------------
function initPerformancePage() {
  const runBtn = document.getElementById('runPerformanceBtn');
  const resultsContainer = document.getElementById('perfBenchmarkResults');

  if (runBtn) {
    runBtn.addEventListener('click', () => {
      runBtn.textContent = 'Running Benchmarks...';
      fetch('/api/performance-benchmark')
        .then(r => r.json())
        .then(res => {
          runBtn.textContent = 'Re-Run Performance Benchmarks';
          let html = '<div class="table-responsive"><table class="custom-table"><thead><tr>';
          html += '<th>Benchmark Test Name</th><th>Rows Returned</th><th>Execution Time (ms)</th><th>Status</th></tr></thead><tbody>';

          res.benchmarks.forEach(item => {
            html += `<tr>
              <td><strong>${item.test_name}</strong></td>
              <td>${item.rows_returned.toLocaleString()}</td>
              <td style="color:#00f2fe;font-weight:700;">${item.execution_time_ms} ms</td>
              <td><span style="color:#10b981;font-weight:700;">${item.status}</span></td>
            </tr>`;
          });
          html += '</tbody></table></div>';
          resultsContainer.innerHTML = html;
        });
    });
  }
}
