/**
 * SkillZen AI v2.0 - Charts & Visualizations
 * Chart.js integration for analytics
 */

class ChartManager {
  constructor() {
    this.charts = {};
    this.colors = {
      primary: '#732C3F',
      secondary: '#C57C8A',
      accent: '#F7E8EC',
      success: '#4CAF50',
      warning: '#FF9800',
      danger: '#F44336',
      info: '#2196F3'
    };
  }

  /**
   * Create line chart
   */
  createLineChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
      console.error(`Canvas ${canvasId} not found`);
      return null;
    }

    // Destroy existing chart if it exists
    if (this.charts[canvasId]) {
      this.charts[canvasId].destroy();
    }

    const defaultOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary'),
            font: {
              size: 12,
              weight: '600'
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: 12,
          titleFont: {
            size: 14,
            weight: '600'
          },
          bodyFont: {
            size: 13
          },
          borderColor: this.colors.secondary,
          borderWidth: 1
        }
      },
      scales: {
        x: {
          grid: {
            color: 'rgba(0, 0, 0, 0.05)',
            drawBorder: false
          },
          ticks: {
            color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
          }
        },
        y: {
          grid: {
            color: 'rgba(0, 0, 0, 0.05)',
            drawBorder: false
          },
          ticks: {
            color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
          },
          beginAtZero: true
        }
      }
    };

    const chartConfig = {
      type: 'line',
      data: data,
      options: { ...defaultOptions, ...options }
    };

    this.charts[canvasId] = new Chart(ctx, chartConfig);
    return this.charts[canvasId];
  }

  /**
   * Create bar chart
   */
  createBarChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
      console.error(`Canvas ${canvasId} not found`);
      return null;
    }

    if (this.charts[canvasId]) {
      this.charts[canvasId].destroy();
    }

    const defaultOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: 12,
          titleFont: {
            size: 14,
            weight: '600'
          },
          bodyFont: {
            size: 13
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
          }
        },
        y: {
          grid: {
            color: 'rgba(0, 0, 0, 0.05)',
            drawBorder: false
          },
          ticks: {
            color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
          },
          beginAtZero: true
        }
      }
    };

    const chartConfig = {
      type: 'bar',
      data: data,
      options: { ...defaultOptions, ...options }
    };

    this.charts[canvasId] = new Chart(ctx, chartConfig);
    return this.charts[canvasId];
  }

  /**
   * Create doughnut chart
   */
  createDoughnutChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
      console.error(`Canvas ${canvasId} not found`);
      return null;
    }

    if (this.charts[canvasId]) {
      this.charts[canvasId].destroy();
    }

    const defaultOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary'),
            padding: 15,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: 12
        }
      }
    };

    const chartConfig = {
      type: 'doughnut',
      data: data,
      options: { ...defaultOptions, ...options }
    };

    this.charts[canvasId] = new Chart(ctx, chartConfig);
    return this.charts[canvasId];
  }

  /**
   * Create radar chart
   */
  createRadarChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    if (this.charts[canvasId]) {
      this.charts[canvasId].destroy();
    }

    const defaultOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          beginAtZero: true,
          ticks: {
            color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          pointLabels: {
            color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary'),
            font: {
              size: 12,
              weight: '600'
            }
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    };

    const chartConfig = {
      type: 'radar',
      data: data,
      options: { ...defaultOptions, ...options }
    };

    this.charts[canvasId] = new Chart(ctx, chartConfig);
    return this.charts[canvasId];
  }

  /**
   * Update chart data
   */
  updateChart(canvasId, newData) {
    if (this.charts[canvasId]) {
      this.charts[canvasId].data = newData;
      this.charts[canvasId].update();
    }
  }

  /**
   * Destroy chart
   */
  destroyChart(canvasId) {
    if (this.charts[canvasId]) {
      this.charts[canvasId].destroy();
      delete this.charts[canvasId];
    }
  }

  /**
   * Generate gradient
   */
  createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
  }

  /**
   * Generate color palette
   */
  generateColorPalette(count) {
    const colors = [
      this.colors.primary,
      this.colors.secondary,
      this.colors.accent,
      this.colors.success,
      this.colors.warning,
      this.colors.danger,
      this.colors.info
    ];

    if (count <= colors.length) {
      return colors.slice(0, count);
    }

    // Generate additional colors if needed
    const palette = [...colors];
    while (palette.length < count) {
      const hue = (palette.length * 137.508) % 360;
      palette.push(`hsl(${hue}, 70%, 60%)`);
    }

    return palette;
  }
}

// Initialize global chart manager
window.chartManager = new ChartManager();