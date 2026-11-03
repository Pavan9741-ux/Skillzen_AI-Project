/**
 * SkillZen AI - Theme Manager
 * Handles dark/light mode toggle
 */

class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem('theme') || 'dark';
    this.init();
  }

  init() {
    // Apply saved theme
    this.applyTheme(this.theme);
    
    // Create theme toggle button
    this.createToggleButton();
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        this.applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  createToggleButton() {
    const existingButton = document.querySelector('.theme-toggle');
    if (existingButton) return;

    const button = document.createElement('button');
    button.className = 'theme-toggle';
    button.setAttribute('aria-label', 'Toggle theme');
    button.innerHTML = this.getIcon();
    button.addEventListener('click', () => this.toggle());
    
    document.body.appendChild(button);
  }

  getIcon() {
    if (this.theme === 'dark') {
      return `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      `;
    } else {
      return `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      `;
    }
  }

  toggle() {
    this.theme = this.theme === 'dark' ? 'light' : 'dark';
    this.applyTheme(this.theme);
    localStorage.setItem('theme', this.theme);
    
    // Update button icon
    const button = document.querySelector('.theme-toggle');
    if (button) {
      button.innerHTML = this.getIcon();
    }
  }

  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.theme = theme;
  }
}

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
  });
} else {
  window.themeManager = new ThemeManager();
}