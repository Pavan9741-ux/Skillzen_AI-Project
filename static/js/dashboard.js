/**
 * SkillZen AI v2.0 - Dashboard Controller
 * Manages analytics dashboard
 */

class DashboardController {
  constructor() {
    this.stats = null;
    this.timeRange = 30; // days
    this.init();
  }

  async init() {
    console.log('🎯 Dashboard initialized');
    
    await this.loadPlatformStats();
    await this.loadSkillTrends();
    await this.loadTimelineData();
    
    this.setupEventListeners();
  }

  /**
   * Load platform statistics
   */
  async loadPlatformStats() {
    try {
      const response = await fetch('/analytics/platform-stats');
      const data = await response.json();
      
      this.stats = data;
      this.renderKPICards(data);
      
    } catch (error) {
      console.error('Error loading platform stats:', error);
      this.showError('Failed to load platform statistics');
    }
  }

  /**
   * Render KPI cards
   */
  renderKPICards(stats) {
    const kpiData = [
      {
        icon: 'fas fa-users',
        value: stats.total_students || 0,
        label: 'Total Students',
        change: '+12%',
        changeType: 'positive'
      },
      {
        icon: 'fas fa-building',
        value: stats.total_companies || 0,
        label: 'Active Companies',
        change: '+5%',
        changeType: 'positive'
      },
      {
        icon: 'fas fa-file-alt',
        value: stats.total_applications || 0,
        label: 'Applications',
        change: '+18%',
        changeType: 'positive'
      },
      {
        icon: 'fas fa-check-circle',
        value: stats.successful_placements || 0,
        label: 'Placements',
        change: `${stats.success_rate || 0}%`,
        changeType: 'positive'
      },
      {
        icon: 'fas fa-chart-line',
        value: `${stats.avg_match_score || 0}%`,
        label: 'Avg Match Score',
        change: '+3%',
        changeType: 'positive'
      },
      {
        icon: 'fas fa-user-check',
        value: `${stats.avg_profile_completeness || 0}%`,
        label: 'Profile Completeness',
        change: '+8%',
        changeType: 'positive'
      }
    ];

    const container = document.getElementById('kpi-container');
    if (!container) return;

    container.innerHTML = kpiData.map(kpi => `
      <div class="kpi-card dashboard-animate">
        <div class="kpi-header">
          <div class="kpi-icon">
            <i class="${kpi.icon}"></i>
          </div>
          <div class="kpi-change ${kpi.changeType}">
            <i class="fas fa-arrow-up"></i>
            ${kpi.change}
          </div>
        </div>
        <div class="kpi-body">
          <div class="kpi-value">${kpi.value}</div>
          <div class="kpi-label">${kpi.label}</div>
        </div>
      </div>
    `).join('');
  }

  /**
   * Load skill trends
   */
  async loadSkillTrends() {
    try {
      const response = await fetch('/analytics/trending-skills');
      const data = await response.json();
      
      this.renderSkillTrends(data.skills || []);
      this.renderTopSkillsChart(data.skills || []);
      
    } catch (error) {
      console.error('Error loading skill trends:', error);
    }
  }

  /**
   * Render skill trends
   */
  renderSkillTrends(skills) {
    const container = document.getElementById('skill-trends-container');
    if (!container) return;

    container.innerHTML = skills.slice(0, 12).map(skill => `
      <div class="trend-item stagger-item">
        <div class="trend-header">
          <div class="trend-name">${skill.name}</div>
          <span class="trend-badge ${skill.status}">${skill.status}</span>
        </div>
        <div class="trend-stats">
          <div class="trend-stat">
            <div class="trend-stat-value">${skill.demand}</div>
            <div class="trend-stat-label">Demand</div>
          </div>
          <div class="trend-stat">
            <div class="trend-stat-value">${skill.students || 0}</div>
            <div class="trend-stat-label">Students</div>
          </div>
        </div>
        <div class="trend-growth ${skill.growth >= 0 ? 'positive' : 'negative'}">
          <i class="fas fa-arrow-${skill.growth >= 0 ? 'up' : 'down'}"></i>
          ${Math.abs(skill.growth).toFixed(1)}%
        </div>
      </div>
    `).join('');
  }

  /**
   * Render top skills chart
   */
  renderTopSkillsChart(skills) {
    const topSkills = skills.slice(0, 10);
    
    const data = {
      labels: topSkills.map(s => s.name),
      datasets: [{
        label: 'Demand Count',
        data: topSkills.map(s => s.demand),
        backgroundColor: window.chartManager.generateColorPalette(topSkills.length),
        borderWidth: 0,
        borderRadius: 8
      }]
    };

    window.chartManager.createBarChart('top-skills-chart', data);
  }

  /**
   * Load timeline data
   */
  async loadTimelineData() {
    try {
      const response = await fetch(`/analytics/timeline?days=${this.timeRange}`);
      const data = await response.json();
      
      this.renderTimelineChart(data.timeline || []);
      
    } catch (error) {
      console.error('Error loading timeline data:', error);
    }
  }

  /**
   * Render timeline chart
   */
  renderTimelineChart(timeline) {
    if (!timeline || timeline.length === 0) return;

    const labels = timeline.map(t => new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    
    const data = {
      labels: labels,
      datasets: [
        {
          label: 'Students',
          data: timeline.map(t => t.students),
          borderColor: '#732C3F',
          backgroundColor: 'rgba(115, 44, 63, 0.1)',
          fill: true,
          tension: 0.4
        },
        {
          label: 'Applications',
          data: timeline.map(t => t.applications),
          borderColor: '#C57C8A',
          backgroundColor: 'rgba(197, 124, 138, 0.1)',
          fill: true,
          tension: 0.4
        },
        {
          label: 'Placements',
          data: timeline.map(t => t.placements),
          borderColor: '#4CAF50',
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          fill: true,
          tension: 0.4
        }
      ]
    };

    window.chartManager.createLineChart('timeline-chart', data);
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Time range filters
    document.querySelectorAll('.chart-filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const range = e.target.dataset.range;
        this.changeTimeRange(parseInt(range));
        
        // Update active state
        document.querySelectorAll('.chart-filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
      });
    });
  }

  /**
   * Change time range
   */
  async changeTimeRange(days) {
    this.timeRange = days;
    await this.loadTimelineData();
  }

  /**
   * Show error message
   */
  showError(message) {
    const notification = document.createElement('div');
    notification.className = 'notification notification-error';
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 2rem;
      right: 2rem;
      background: var(--glass-bg);
      border: 1px solid #F44336;
      border-radius: 12px;
      padding: 1rem 2rem;
      z-index: 10000;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 3000);
  }
}

// Initialize dashboard when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('kpi-container')) {
      window.dashboardController = new DashboardController();
    }
  });
} else {
  if (document.getElementById('kpi-container')) {
    window.dashboardController = new DashboardController();
  }
}