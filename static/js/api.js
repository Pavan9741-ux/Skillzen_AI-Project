/**
 * SkillZen AI - API Client
 * Handles all API communications
 */

class SkillZenAPI {
  constructor() {
    this.baseURL = window.location.origin;
  }

  /**
   * Generic API request handler
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin',
    };

    const config = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  /**
   * Get platform health status
   */
  async getHealth() {
    return this.request('/api/health');
  }

  /**
   * Get platform statistics
   */
  async getStats() {
    return this.request('/api/stats');
  }

  /**
   * Get all available skills and languages
   */
  async getAllSkills() {
    return this.request('/student/skills/all');
  }

  /**
   * Get personalized recommendations
   */
  async getRecommendations(studentData) {
    return this.request('/student/recommend', {
      method: 'POST',
      body: JSON.stringify(studentData),
    });
  }

  /**
   * Admin login
   */
  async login(username, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  /**
   * Admin logout
   */
  async logout() {
    return this.request('/auth/logout', {
      method: 'POST',
    });
  }

  /**
   * Check authentication status
   */
  async checkAuth() {
    return this.request('/auth/check');
  }

  /**
   * Get all companies (admin only)
   */
  async getCompanies() {
    return this.request('/admin/companies');
  }

  /**
   * Add new company (admin only)
   */
  async addCompany(companyData) {
    return this.request('/admin/companies', {
      method: 'POST',
      body: JSON.stringify(companyData),
    });
  }

  /**
   * Update company (admin only)
   */
  async updateCompany(companyId, companyData) {
    return this.request(`/admin/companies/${companyId}`, {
      method: 'PUT',
      body: JSON.stringify(companyData),
    });
  }

  /**
   * Delete company (admin only)
   */
  async deleteCompany(companyId) {
    return this.request(`/admin/companies/${companyId}`, {
      method: 'DELETE',
    });
  }
}

// Create global API instance
window.api = new SkillZenAPI();