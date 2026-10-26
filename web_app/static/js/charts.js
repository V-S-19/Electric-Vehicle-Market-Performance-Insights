/**
 * Charting Engine for EV Market Analytics
 * Built on Chart.js with custom glowing gradients, dark mode aesthetics, and dynamic animations.
 */

// Global Chart Registry
const EVCharts = {
  instances: {},

  colors: {
    cyan: '#00f2fe',
    electricBlue: '#4facfe',
    emerald: '#10b981',
    purple: '#a855f7',
    amber: '#f59e0b',
    rose: '#f43f5e',
    grid: 'rgba(255, 255, 255, 0.06)',
    text: '#94a3b8'
  },

  palette: ['#00f2fe', '#4facfe', '#a855f7', '#10b981', '#f59e0b', '#ec4899', '#38bdf8', '#818cf8'],

  initYearlyChart(ctx, yearlyData) {
    if (this.instances.yearly) this.instances.yearly.destroy();
    if (!ctx) return;

    const labels = yearlyData.model_year || [2019, 2020, 2021, 2022, 2023, 2024, 2025];
    const sales = yearlyData.annual_sales_units || [];
    const revenue = yearlyData.total_revenue_usd ? yearlyData.total_revenue_usd.map(v => v / 1e9) : [];

    this.instances.yearly = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Sales Volume (Units)',
            data: sales,
            borderColor: this.colors.cyan,
            backgroundColor: 'rgba(0, 242, 254, 0.12)',
            fill: true,
            tension: 0.35,
            yAxisID: 'y'
          },
          {
            label: 'Revenue ($ Billions)',
            data: revenue,
            borderColor: this.colors.purple,
            backgroundColor: 'transparent',
            borderDash: [5, 5],
            tension: 0.35,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { labels: { color: this.colors.text } },
          tooltip: {
            backgroundColor: '#0e1526',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1
          }
        },
        scales: {
          x: { grid: { color: this.colors.grid }, ticks: { color: this.colors.text } },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            grid: { color: this.colors.grid },
            ticks: { color: this.colors.text }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { color: this.colors.purple }
          }
        }
      }
    });
  },

  initCategoryDonut(ctx, catData) {
    if (this.instances.category) this.instances.category.destroy();
    if (!ctx) return;

    const labels = Object.keys(catData);
    const data = Object.values(catData);

    this.instances.category = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: this.palette.slice(0, labels.length),
          borderColor: '#0e1526',
          borderWidth: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: this.colors.text, boxWidth: 12 } }
        },
        cutout: '68%'
      }
    });
  },

  initManufacturerBar(ctx, mfgData) {
    if (this.instances.manufacturer) this.instances.manufacturer.destroy();
    if (!ctx) return;

    const labels = Object.keys(mfgData);
    const data = Object.values(mfgData);

    this.instances.manufacturer = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Total Units Sold',
          data: data,
          backgroundColor: 'rgba(79, 172, 254, 0.75)',
          borderColor: this.colors.electricBlue,
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { grid: { color: this.colors.grid }, ticks: { color: this.colors.text } },
          y: { grid: { display: false }, ticks: { color: this.colors.text } }
        }
      }
    });
  },

  initBatteryRadar(ctx, batteryData) {
    if (this.instances.battery) this.instances.battery.destroy();
    if (!ctx) return;

    const labels = Object.keys(batteryData);
    const ranges = labels.map(l => batteryData[l].driving_range_km);
    const fastCharges = labels.map(l => batteryData[l].fast_charging_time_min);

    this.instances.battery = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Avg Range (km)',
            data: ranges,
            backgroundColor: 'rgba(0, 242, 254, 0.7)',
            borderRadius: 6
          },
          {
            label: 'Fast Charge (mins)',
            data: fastCharges,
            backgroundColor: 'rgba(245, 158, 11, 0.7)',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: this.colors.text } }
        },
        scales: {
          x: { grid: { color: this.colors.grid }, ticks: { color: this.colors.text } },
          y: { grid: { color: this.colors.grid }, ticks: { color: this.colors.text } }
        }
      }
    });
  },

  initRegionBar(ctx, regionData) {
    if (this.instances.region) this.instances.region.destroy();
    if (!ctx) return;

    const labels = Object.keys(regionData);
    const data = Object.values(regionData);

    this.instances.region = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: ['#10b981', '#4facfe', '#a855f7', '#f59e0b', '#f43f5e'],
          borderColor: '#0e1526',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'right', labels: { color: this.colors.text, boxWidth: 12 } }
        }
      }
    });
  },

  initRangePriceScatter(ctx, catRangePrice) {
    if (this.instances.rangePrice) this.instances.rangePrice.destroy();
    if (!ctx) return;

    const labels = Object.keys(catRangePrice);
    const ranges = labels.map(l => catRangePrice[l].driving_range_km);
    const prices = labels.map(l => catRangePrice[l].base_price_usd / 1000); // in $K

    this.instances.rangePrice = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Avg Driving Range (km)',
            data: ranges,
            backgroundColor: 'rgba(16, 185, 129, 0.8)',
            borderRadius: 6,
            yAxisID: 'y'
          },
          {
            label: 'Avg Base Price ($K)',
            data: prices,
            backgroundColor: 'rgba(236, 72, 153, 0.8)',
            borderRadius: 6,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: this.colors.text } }
        },
        scales: {
          x: { grid: { color: this.colors.grid }, ticks: { color: this.colors.text } },
          y: {
            type: 'linear',
            position: 'left',
            grid: { color: this.colors.grid },
            ticks: { color: this.colors.text }
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { color: '#ec4899' }
          }
        }
      }
    });
  }
};
