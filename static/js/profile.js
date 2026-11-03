/**
 * SkillZen AI v2.0 - Profile Manager
 * Manages student profile page
 */

class ProfileManager {
  constructor(userId) {
    this.userId = userId;
    this.profile = null;
    this.editMode = false;
    this.init();
  }

  async init() {
    console.log('👤 Profile Manager initialized');
    
    await this.loadProfile();
    this.setupEventListeners();
  }

  /**
   * Load profile data
   */
  async loadProfile() {
    try {
      const response = await fetch(`/profile/${this.userId}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          this.showCreateProfilePrompt();
          return;
        }
        throw new Error('Failed to load profile');
      }
      
      const data = await response.json();
      this.profile = data.profile;
      
      this.renderProfile(this.profile);
      this.renderProfileStats(this.profile);
      this.renderSkills(this.profile);
      this.renderProjects(this.profile);
      this.renderCertifications(this.profile);
      
    } catch (error) {
      console.error('Error loading profile:', error);
      this.showError('Failed to load profile');
    }
  }

  /**
   * Render profile header
   */
  renderProfile(profile) {
    const container = document.getElementById('profile-header-content');
    if (!container) return;

    const initials = profile.full_name 
      ? profile.full_name.split(' ').map(n => n[0]).join('').toUpperCase()
      : '?';

    container.innerHTML = `
      <div class="profile-avatar-wrapper">
        ${profile.avatar_url 
          ? `<img src="${profile.avatar_url}" alt="${profile.full_name}" class="profile-avatar">`
          : `<div class="profile-avatar">${initials}</div>`
        }
        <button class="avatar-upload-btn" onclick="profileManager.uploadAvatar()">
          <i class="fas fa-camera"></i>
        </button>
      </div>
      <div class="profile-info">
        <h1 class="profile-name">${profile.full_name || 'Your Name'}</h1>
        <div class="profile-meta">
          <div class="profile-meta-item">
            <i class="fas fa-graduation-cap"></i>
            <span>${profile.branch || 'Branch'} - Semester ${profile.semester || 'N/A'}</span>
          </div>
          <div class="profile-meta-item">
            <i class="fas fa-university"></i>
            <span>${profile.college || 'College Name'}</span>
          </div>
          <div class="profile-meta-item">
            <i class="fas fa-chart-line"></i>
            <span>CGPA: ${profile.cgpa ? profile.cgpa.toFixed(2) : 'N/A'}</span>
          </div>
          ${profile.email ? `
            <div class="profile-meta-item">
              <i class="fas fa-envelope"></i>
              <span>${profile.email}</span>
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }

  /**
   * Render profile statistics
   */
  renderProfileStats(profile) {
    const statsContainer = document.getElementById('profile-stats');
    if (!statsContainer) return;

    statsContainer.innerHTML = `
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-eye"></i>
        </div>
        <div class="stat-value">${profile.profile_views || 0}</div>
        <div class="stat-label">Profile Views</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-paper-plane"></i>
        </div>
        <div class="stat-value">${profile.applications_sent || 0}</div>
        <div class="stat-label">Applications</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-check-circle"></i>
        </div>
        <div class="stat-value">${profile.applications_accepted || 0}</div>
        <div class="stat-label">Accepted</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-percentage"></i>
        </div>
        <div class="stat-value">${profile.profile_completeness ? profile.profile_completeness.toFixed(0) : 0}%</div>
        <div class="stat-label">Completeness</div>
      </div>
    `;

    // Render completeness card
    this.renderCompletenessCard(profile);
  }

  /**
   * Render profile completeness
   */
  renderCompletenessCard(profile) {
    const container = document.getElementById('completeness-card');
    if (!container) return;

    const completeness = profile.profile_completeness || 0;
    const missingFields = this.getMissingFields(profile);

    container.innerHTML = `
      <div class="completeness-header">
        <h3>Profile Completeness</h3>
        <div class="completeness-percentage">${completeness.toFixed(0)}%</div>
      </div>
      <div class="progress-bar-container">
        <div class="progress-bar" style="width: ${completeness}%"></div>
      </div>
      ${missingFields.length > 0 ? `
        <div class="missing-fields">
          <strong>Missing:</strong>
          ${missingFields.map(field => `
            <span class="missing-field-tag">${field}</span>
          `).join('')}
        </div>
      ` : `
        <div style="margin-top: 1rem; color: var(--theme-secondary);">
          <i class="fas fa-check-circle"></i> Profile is complete!
        </div>
      `}
    `;
  }

  /**
   * Get missing profile fields
   */
  getMissingFields(profile) {
    const fields = [];
    
    if (!profile.avatar_url) fields.push('Avatar');
    if (!profile.phone) fields.push('Phone');
    if (!profile.github_url) fields.push('GitHub');
    if (!profile.linkedin_url) fields.push('LinkedIn');
    if (!profile.resume_url) fields.push('Resume');
    if (!profile.projects || profile.projects.length === 0) fields.push('Projects');
    if (!profile.certifications || profile.certifications.length === 0) fields.push('Certifications');
    
    return fields;
  }

  /**
   * Render skills
   */
  renderSkills(profile) {
    // Technical skills
    const techContainer = document.getElementById('technical-skills');
    if (techContainer && profile.technical_skills) {
      techContainer.innerHTML = `
        <h4 style="margin-bottom: 1rem;">Technical Skills</h4>
        <div class="skills-grid">
          ${profile.technical_skills.map(skill => `
            <div class="skill-tag verified">${skill}</div>
          `).join('')}
        </div>
      `;
    }

    // Programming languages
    const langContainer = document.getElementById('programming-languages');
    if (langContainer && profile.programming_languages) {
      langContainer.innerHTML = `
        <h4 style="margin-bottom: 1rem;">Programming Languages</h4>
        <div class="skills-grid">
          ${profile.programming_languages.map(lang => `
            <div class="skill-tag">${lang}</div>
          `).join('')}
        </div>
      `;
    }

    // Non-technical skills
    const softContainer = document.getElementById('soft-skills');
    if (softContainer && profile.non_technical_skills) {
      softContainer.innerHTML = `
        <h4 style="margin-bottom: 1rem;">Soft Skills</h4>
        <div class="skills-grid">
          ${profile.non_technical_skills.map(skill => `
            <div class="skill-tag">${skill}</div>
          `).join('')}
        </div>
      `;
    }
  }

  /**
   * Render projects
   */
  renderProjects(profile) {
    const container = document.getElementById('projects-list');
    if (!container) return;

    if (!profile.projects || profile.projects.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
          <i class="fas fa-folder-open" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
          <p>No projects added yet</p>
          <button class="btn btn-premium" onclick="profileManager.addProject()">
            Add Project
          </button>
        </div>
      `;
      return;
    }

    container.innerHTML = profile.projects.map(project => `
      <div class="project-item">
        <div class="project-header">
          <h4 class="project-title">${project.name}</h4>
          ${project.link ? `
            <a href="${project.link}" target="_blank" class="project-link">
              <i class="fas fa-external-link-alt"></i>
            </a>
          ` : ''}
        </div>
        <p class="project-description">${project.description}</p>
        ${project.technologies ? `
          <div class="project-tech">
            ${project.technologies.map(tech => `
              <span class="tech-badge">${tech}</span>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `).join('');
  }

  /**
   * Render certifications
   */
  renderCertifications(profile) {
    const container = document.getElementById('certifications-list');
    if (!container) return;

    if (!profile.certifications || profile.certifications.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
          <i class="fas fa-certificate" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
          <p>No certifications added yet</p>
          <button class="btn btn-premium" onclick="profileManager.addCertification()">
            Add Certification
          </button>
        </div>
      `;
      return;
    }

    container.innerHTML = profile.certifications.map(cert => `
      <div class="certification-item">
        <div class="cert-icon">
          <i class="fas fa-award"></i>
        </div>
        <div class="cert-info">
          <div class="cert-name">${cert.name}</div>
          <div class="cert-issuer">${cert.issuer} ${cert.date ? `• ${cert.date}` : ''}</div>
        </div>
      </div>
    `).join('');
  }

  /**
   * Upload avatar
   */
  async uploadAvatar() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    
    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('avatar', file);

      try {
        const response = await fetch(`/profile/${this.userId}/avatar`, {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const data = await response.json();
          this.showSuccess('Avatar uploaded successfully!');
          await this.loadProfile();
        } else {
          throw new Error('Upload failed');
        }
      } catch (error) {
        console.error('Error uploading avatar:', error);
        this.showError('Failed to upload avatar');
      }
    };

    input.click();
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Edit mode toggle
    const editBtn = document.getElementById('edit-mode-toggle');
    if (editBtn) {
      editBtn.addEventListener('click', () => this.toggleEditMode());
    }
  }

  /**
   * Toggle edit mode
   */
  toggleEditMode() {
    this.editMode = !this.editMode;
    
    if (this.editMode) {
      this.showEditForm();
    } else {
      this.hideEditForm();
    }
  }

  /**
   * Show success message
   */
  showSuccess(message) {
    this.showNotification(message, 'success');
  }

  /**
   * Show error message
   */
  showError(message) {
    this.showNotification(message, 'error');
  }

  /**
   * Show notification
   */
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} slide-in-down`;
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 2rem;
      right: 2rem;
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      border-radius: 12px;
      padding: 1rem 2rem;
      z-index: 10000;
      color: var(--text-primary);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.classList.add('fade-out');
      setTimeout(() => notification.remove(), 500);
    }, 3000);
  }

  /**
   * Show create profile prompt
   */
  showCreateProfilePrompt() {
    const container = document.getElementById('main-content');
    if (!container) return;

    container.innerHTML = `
      <div style="text-align: center; padding: 4rem;">
        <i class="fas fa-user-plus" style="font-size: 5rem; color: var(--theme-secondary); margin-bottom: 2rem;"></i>
        <h2>Welcome to SkillZen AI!</h2>
        <p style="margin: 1rem 0 2rem 0; color: var(--text-secondary);">
          Create your profile to get personalized internship recommendations
        </p>
        <button class="btn btn-premium" onclick="window.location.href='/student'">
          Create Profile
        </button>
      </div>
    `;
  }
}

// Initialize profile manager
window.profileManager = null;