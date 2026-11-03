/**
 * SkillZen AI - Main Application Logic
 * FIXED VERSION - Recommendations working
 */

class SkillZenApp {
  constructor() {
    this.currentStep = 1;
    this.totalSteps = 4;
    this.studentData = {
      cgpa: 7.0,
      sgpa: 7.0,
      technical_skills: [],
      non_technical_skills: [],
      programming_languages: []
    };
    this.allSkills = null;
    this.recommendations = null;
    
    this.init();
  }

  async init() {
    console.log('🚀 SkillZen AI Initialized');
    
    // Load all available skills
    await this.loadSkills();
    
    // Setup event listeners
    this.setupEventListeners();
    
    // Initialize first step
    this.showStep(1);
  }

  /**
   * Load all skills from API
   */
  async loadSkills() {
    try {
      this.allSkills = await window.api.getAllSkills();
      console.log('✅ Skills loaded:', this.allSkills);
    } catch (error) {
      console.error('❌ Failed to load skills:', error);
      this.showNotification('Failed to load skills. Please refresh the page.', 'error');
    }
  }

  /**
   * Setup all event listeners
   */
  setupEventListeners() {
    // CGPA slider
    const cgpaSlider = document.getElementById('cgpa-slider');
    const cgpaValue = document.getElementById('cgpa-value');
    if (cgpaSlider && cgpaValue) {
      cgpaSlider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        cgpaValue.textContent = value.toFixed(1);
        this.studentData.cgpa = value;
      });
    }

    // SGPA slider
    const sgpaSlider = document.getElementById('sgpa-slider');
    const sgpaValue = document.getElementById('sgpa-value');
    if (sgpaSlider && sgpaValue) {
      sgpaSlider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        sgpaValue.textContent = value.toFixed(1);
        this.studentData.sgpa = value;
      });
    }

    // Next/Previous buttons
    document.querySelectorAll('[data-action="next"]').forEach(btn => {
      btn.addEventListener('click', () => this.nextStep());
    });

    document.querySelectorAll('[data-action="prev"]').forEach(btn => {
      btn.addEventListener('click', () => this.prevStep());
    });

    // Submit button
    const submitBtn = document.querySelector('[data-action="submit"]');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => this.submitForm());
    }

    // Restart button
    document.querySelectorAll('[data-action="restart"]').forEach(btn => {
      btn.addEventListener('click', () => this.restart());
    });
  }

  /**
   * Show specific step
   */
  showStep(stepNumber) {
    // Hide all steps
    document.querySelectorAll('.form-step').forEach(step => {
      step.classList.add('hidden');
    });

    // Show current step
    const currentStepEl = document.querySelector(`[data-step="${stepNumber}"]`);
    if (currentStepEl) {
      currentStepEl.classList.remove('hidden');
      currentStepEl.classList.add('fade-in');
    }

    // Update progress bar
    this.updateProgressBar(stepNumber);

    // Render step content if needed
    if (stepNumber === 2) {
      this.renderLanguages();
    } else if (stepNumber === 3) {
      this.renderSkills();
    }

    this.currentStep = stepNumber;
  }

  /**
   * Update progress bar
   */
  updateProgressBar(step) {
    document.querySelectorAll('.progress-step').forEach((el, index) => {
      const stepNum = index + 1;
      el.classList.remove('active', 'completed');
      
      if (stepNum === step) {
        el.classList.add('active');
      } else if (stepNum < step) {
        el.classList.add('completed');
      }
    });
  }

  /**
   * Render programming languages
   */
  renderLanguages() {
    const container = document.getElementById('languages-container');
    if (!container || !this.allSkills) return;

    container.innerHTML = '';
    
    this.allSkills.programming_languages.forEach(lang => {
      const isChecked = this.studentData.programming_languages.includes(lang);
      
      const div = document.createElement('div');
      div.className = 'checkbox-item';
      div.innerHTML = `
        <input type="checkbox" id="lang-${lang}" value="${lang}" ${isChecked ? 'checked' : ''}>
        <label for="lang-${lang}" class="checkbox-label">${lang}</label>
      `;
      
      const checkbox = div.querySelector('input');
      checkbox.addEventListener('change', (e) => {
        if (e.target.checked) {
          if (!this.studentData.programming_languages.includes(lang)) {
            this.studentData.programming_languages.push(lang);
          }
        } else {
          const index = this.studentData.programming_languages.indexOf(lang);
          if (index > -1) {
            this.studentData.programming_languages.splice(index, 1);
          }
        }
        console.log('Languages:', this.studentData.programming_languages);
      });
      
      container.appendChild(div);
    });
  }

  /**
   * Render skills selection
   */
  renderSkills() {
    this.renderSkillCategory('technical', 'Technical Skills');
    this.renderSkillCategory('non-technical', 'Non-Technical Skills');
  }

  renderSkillCategory(type, title) {
    const containerId = type === 'technical' ? 'technical-skills-container' : 'non-technical-skills-container';
    const container = document.getElementById(containerId);
    if (!container || !this.allSkills) return;

    container.innerHTML = `<h3 class="mb-3">${title}</h3>`;
    
    const grid = document.createElement('div');
    grid.className = 'skill-grid';
    
    const skillsArray = type === 'technical' 
      ? this.allSkills.technical_skills 
      : this.allSkills.non_technical_skills;
    
    const studentSkills = type === 'technical'
      ? this.studentData.technical_skills
      : this.studentData.non_technical_skills;
    
    skillsArray.forEach(skill => {
      const isChecked = studentSkills.includes(skill);
      
      const div = document.createElement('div');
      div.className = 'skill-chip';
      div.innerHTML = `
        <input type="checkbox" id="${type}-${skill}" value="${skill}" ${isChecked ? 'checked' : ''}>
        <label for="${type}-${skill}" class="skill-label">${skill}</label>
      `;
      
      const checkbox = div.querySelector('input');
      checkbox.addEventListener('change', (e) => {
        if (e.target.checked) {
          if (!studentSkills.includes(skill)) {
            studentSkills.push(skill);
          }
        } else {
          const index = studentSkills.indexOf(skill);
          if (index > -1) {
            studentSkills.splice(index, 1);
          }
        }
        console.log(`${type} skills:`, studentSkills);
      });
      
      grid.appendChild(div);
    });
    
    container.appendChild(grid);
  }

  /**
   * Validate current step
   */
  validateStep(step) {
    if (step === 1) {
      if (this.studentData.cgpa < 0 || this.studentData.cgpa > 10) {
        this.showNotification('Please enter a valid CGPA (0-10)', 'error');
        return false;
      }
      return true;
    } else if (step === 2) {
      if (this.studentData.programming_languages.length === 0) {
        this.showNotification('Please select at least one programming language', 'error');
        return false;
      }
      return true;
    } else if (step === 3) {
      if (this.studentData.technical_skills.length === 0) {
        this.showNotification('Please select at least one technical skill', 'error');
        return false;
      }
      return true;
    }
    return true;
  }

  /**
   * Go to next step
   */
  nextStep() {
    if (this.validateStep(this.currentStep)) {
      if (this.currentStep < this.totalSteps) {
        this.showStep(this.currentStep + 1);
      }
    }
  }

  /**
   * Go to previous step
   */
  prevStep() {
    if (this.currentStep > 1) {
      this.showStep(this.currentStep - 1);
    }
  }

  /**
   * Submit form and get recommendations
   */
  async submitForm() {
    if (!this.validateStep(3)) {
      return;
    }

    console.log('📤 Submitting data:', this.studentData);
    this.showLoading(true);

    try {
      const response = await window.api.getRecommendations(this.studentData);
      
      console.log('📥 Received response:', response);
      
      if (response && response.recommendations) {
        this.recommendations = response.recommendations;
        this.renderResults(response);
        this.showStep(4);
        this.showNotification('Recommendations loaded successfully!', 'success');
      } else {
        throw new Error('Invalid response format');
      }
      
    } catch (error) {
      console.error('❌ Error:', error);
      this.showNotification('Failed to get recommendations. Please try again.', 'error');
    } finally {
      this.showLoading(false);
    }
  }

  /**
   * Render results
   */
  renderResults(response) {
    const container = document.getElementById('results-container');
    if (!container) return;

    // Statistics
    const statsHtml = `
      <div class="glass-card mb-4 text-center">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem;">
          <div>
            <h3 style="font-size: 2.5rem; margin: 0;">${response.total_companies}</h3>
            <p style="margin: 0; color: var(--text-secondary);">Total Companies</p>
          </div>
          <div>
            <h3 style="font-size: 2.5rem; margin: 0; color: var(--accent-color);">${response.eligible_companies}</h3>
            <p style="margin: 0; color: var(--text-secondary);">Eligible Matches</p>
          </div>
          <div>
            <h3 style="font-size: 2.5rem; margin: 0;">${response.recommendations[0]?.scores?.total_score?.toFixed(1) || 0}%</h3>
            <p style="margin: 0; color: var(--text-secondary);">Top Match Score</p>
          </div>
        </div>
      </div>
    `;

    // Company cards
    const companiesHtml = response.recommendations.slice(0, 10).map((rec, index) => 
      this.createCompanyCard(rec, index)
    ).join('');

    container.innerHTML = statsHtml + companiesHtml;
  }

  /**
   * Create company card HTML
   */
  createCompanyCard(recommendation, index) {
    const { company, scores, gap_analysis, eligible } = recommendation;
    
    const matchColor = scores.total_score >= 80 ? '#4facfe' : 
                       scores.total_score >= 60 ? '#f093fb' : '#f5576c';
    
    return `
      <div class="company-card liquid-glass" data-index="${index}" style="margin-bottom: 2rem;">
        <div class="company-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <div>
            <h3 class="company-name" style="margin: 0; font-size: 1.5rem;">${company.name}</h3>
            <p style="color: var(--text-muted); margin: 0.5rem 0 0 0;">
              📍 ${company.location || 'Location not specified'}
            </p>
          </div>
          <div class="match-score" style="font-size: 2rem; font-weight: 700; color: ${matchColor};">
            ${scores.total_score.toFixed(1)}%
          </div>
        </div>

        <div class="company-details" style="margin: 1rem 0;">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div>
              <strong>Min CGPA:</strong> ${company.min_cgpa}
            </div>
            <div>
              <strong>Duration:</strong> ${company.duration || 'Not specified'}
            </div>
            <div>
              <strong>Stipend:</strong> ₹${company.stipend_range || 'Negotiable'}
            </div>
          </div>
        </div>

        <div style="margin: 1.5rem 0;">
          <strong style="display: block; margin-bottom: 0.5rem;">Skills Match:</strong>
          <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            ${scores.tech_skills_matched.slice(0, 5).map(skill => 
              `<span style="padding: 0.25rem 0.75rem; background: rgba(79, 172, 254, 0.2); border: 1px solid rgba(79, 172, 254, 0.5); border-radius: 8px; font-size: 0.85rem; color: #4facfe;">✓ ${skill}</span>`
            ).join('')}
            ${scores.tech_skills_missing.slice(0, 3).map(skill => 
              `<span style="padding: 0.25rem 0.75rem; background: rgba(245, 87, 108, 0.2); border: 1px solid rgba(245, 87, 108, 0.5); border-radius: 8px; font-size: 0.85rem; color: #f5576c;">✗ ${skill}</span>`
            ).join('')}
          </div>
        </div>

        ${this.createGapAnalysisHTML(gap_analysis)}

        <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
          <button class="btn btn-primary" style="flex: 1;" onclick="window.open('${company.website}', '_blank')">
            Apply Now
          </button>
          <button class="btn btn-glass" onclick="app.toggleDetails(${index})">
            View Details
          </button>
        </div>

        <div id="details-${index}" class="hidden" style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--glass-border);">
          <h4>Contact Information</h4>
          <p><strong>Email:</strong> ${company.email || 'Not provided'}</p>
          <p><strong>Phone:</strong> ${company.phone || 'Not provided'}</p>
          <p><strong>Website:</strong> <a href="${company.website}" target="_blank" style="color: var(--accent-color);">${company.website}</a></p>
        </div>
      </div>
    `;
  }

  /**
   * Create gap analysis HTML
   */
  createGapAnalysisHTML(gap_analysis) {
    if (!gap_analysis) return '';

    if (gap_analysis.overall_match >= 95) {
      return `
        <div style="margin-top: 1rem; padding: 1rem; background: rgba(79, 172, 254, 0.1); border-left: 4px solid #4facfe; border-radius: 8px;">
          <h4 style="margin: 0 0 0.5rem 0; color: #4facfe;">🎉 Perfect Match!</h4>
          <p style="margin: 0;">You meet all requirements for this company!</p>
        </div>
      `;
    }

    let html = '<div style="margin-top: 1rem; padding: 1rem; background: var(--glass-bg-secondary); border-left: 4px solid var(--accent-color); border-radius: 8px;">';
    html += '<h4 style="margin: 0 0 1rem 0;">📊 Skill Gap Analysis</h4>';

    // Priority Actions
    if (gap_analysis.priority_actions && gap_analysis.priority_actions.length > 0) {
      html += '<div style="margin-bottom: 1rem;"><strong>Priority Actions:</strong></div>';
      gap_analysis.priority_actions.slice(0, 3).forEach(action => {
        const colorMap = { HIGH: '#f5576c', MEDIUM: '#f093fb', LOW: '#4facfe' };
        const color = colorMap[action.priority] || '#4facfe';
        html += `
          <div style="padding: 0.75rem; margin-bottom: 0.5rem; background: var(--glass-bg-primary); border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
            <span>
              <span style="padding: 0.25rem 0.5rem; background: ${color}20; color: ${color}; border-radius: 4px; font-size: 0.75rem; font-weight: 700; margin-right: 0.5rem;">${action.priority}</span>
              ${action.action}
            </span>
            <span style="color: var(--text-muted); font-size: 0.85rem;">${action.impact}</span>
          </div>
        `;
      });
    }

    html += '</div>';
    return html;
  }

  /**
   * Toggle company details
   */
  toggleDetails(index) {
    const details = document.getElementById(`details-${index}`);
    if (details) {
      details.classList.toggle('hidden');
    }
  }

  /**
   * Show loading overlay
   */
  showLoading(show) {
    let overlay = document.getElementById('loading-overlay');
    
    if (show) {
      if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
          <div class="spinner"></div>
          <div class="loading-text">Finding your perfect matches<span class="loading-dots"></span></div>
        `;
        document.body.appendChild(overlay);
      }
      overlay.classList.remove('hidden');
      overlay.style.display = 'flex';
    } else {
      if (overlay) {
        overlay.classList.add('hidden');
        overlay.style.display = 'none';
      }
    }
  }

  /**
   * Show notification
   */
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} slide-in-down`;
    notification.style.cssText = `
      position: fixed;
      top: 2rem;
      right: 2rem;
      padding: 1rem 2rem;
      background: var(--glass-bg-primary);
      backdrop-filter: blur(20px);
      border: 1px solid var(--glass-border);
      border-radius: 12px;
      box-shadow: var(--shadow-lg);
      z-index: 10000;
      max-width: 400px;
      color: var(--text-primary);
    `;
    
    const color = type === 'error' ? '#f5576c' : type === 'success' ? '#4facfe' : '#f093fb';
    notification.style.borderLeft = `4px solid ${color}`;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.classList.add('fade-out');
      setTimeout(() => notification.remove(), 500);
    }, 3000);
  }

  /**
   * Restart the application
   */
  restart() {
    this.studentData = {
      cgpa: 7.0,
      sgpa: 7.0,
      technical_skills: [],
      non_technical_skills: [],
      programming_languages: []
    };
    this.recommendations = null;
    this.showStep(1);
    
    // Reset sliders
    const cgpaSlider = document.getElementById('cgpa-slider');
    const sgpaSlider = document.getElementById('sgpa-slider');
    if (cgpaSlider) {
      cgpaSlider.value = 7.0;
      document.getElementById('cgpa-value').textContent = '7.0';
    }
    if (sgpaSlider) {
      sgpaSlider.value = 7.0;
      document.getElementById('sgpa-value').textContent = '7.0';
    }
  }
}

// Initialize app when DOM is ready
let app;
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    app = new SkillZenApp();
    window.app = app;
  });
} else {
  app = new SkillZenApp();
  window.app = app;
}