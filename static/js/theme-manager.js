/**
 * SkillZen AI - Advanced Theme Manager
 * Handles theme switching and persistence
 */

class ThemeManager {
  constructor() {
    this.themes = {
      'obsidian-rose': {
        name: 'Obsidian Rose',
        colors: ['#732C3F', '#C57C8A', '#F7E8EC']
      },
      'midnight-ocean': {
        name: 'Midnight Ocean',
        colors: ['#0A1929', '#1E3A5F', '#4FC3F7']
      },
      'purple-dream': {
        name: 'Purple Dream',
        colors: ['#5E35B1', '#9575CD', '#E1BEE7']
      },
      'forest-green': {
        name: 'Forest Green',
        colors: ['#1B5E20', '#4CAF50', '#A5D6A7']
      },
      'sunset-orange': {
        name: 'Sunset Orange',
        colors: ['#E65100', '#FF6F00', '#FFE0B2']
      },
      'arctic-blue': {
        name: 'Arctic Blue',
        colors: ['#006064', '#00ACC1', '#B2EBF2']
      }
    };
    
    this.currentTheme = this.loadTheme();
    this.init();
  }

  init() {
    this.applyTheme(this.currentTheme);
    this.createThemeSelector();
    this.setupEventListeners();
  }

  loadTheme() {
    return localStorage.getItem('skillzen-theme') || 'obsidian-rose';
  }

  saveTheme(theme) {
    localStorage.setItem('skillzen-theme', theme);
  }

  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.currentTheme = theme;
    this.saveTheme(theme);
    
    // Update meta theme color for mobile browsers
    const metaTheme = document.querySelector('meta[name="theme-color"]');
    if (metaTheme) {
      metaTheme.setAttribute('content', this.themes[theme].colors[0]);
    }
    
    // Animate theme change
    document.body.style.animation = 'themeTransition 0.5s ease';
    setTimeout(() => {
      document.body.style.animation = '';
    }, 500);
  }

  createThemeSelector() {
    const selector = document.createElement('div');
    selector.className = 'theme-selector';
    selector.innerHTML = `
      <button class="theme-toggle-btn" aria-label="Change Theme">
        <i class="fas fa-palette"></i>
      </button>
      <div class="theme-options">
        ${Object.entries(this.themes).map(([key, theme]) => `
          <div class="theme-option ${key === this.currentTheme ? 'active' : ''}" data-theme="${key}">
            <div class="theme-preview" style="background: linear-gradient(135deg, ${theme.colors[0]} 0%, ${theme.colors[1]} 50%, ${theme.colors[2]} 100%);"></div>
            <span class="theme-name">${theme.name}</span>
          </div>
        `).join('')}
      </div>
    `;
    
    document.body.appendChild(selector);
  }

  setupEventListeners() {
    const toggleBtn = document.querySelector('.theme-toggle-btn');
    const options = document.querySelector('.theme-options');
    
    toggleBtn.addEventListener('click', () => {
      options.classList.toggle('active');
    });
    
    document.querySelectorAll('.theme-option').forEach(option => {
      option.addEventListener('click', (e) => {
        const theme = e.currentTarget.dataset.theme;
        this.applyTheme(theme);
        
        // Update active state
        document.querySelectorAll('.theme-option').forEach(opt => {
          opt.classList.remove('active');
        });
        e.currentTarget.classList.add('active');
        
        // Close menu
        options.classList.remove('active');
        
        // Show notification
        this.showNotification(`Theme changed to ${this.themes[theme].name}`);
      });
    });
    
    // Close theme menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.theme-selector')) {
        options.classList.remove('active');
      }
    });
  }

  showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'theme-notification';
    notification.style.cssText = `
      position: fixed;
      top: 2rem;
      left: 50%;
      transform: translateX(-50%);
      background: var(--glass-bg);
      backdrop-filter: blur(20px);
      border: 1px solid var(--glass-border);
      border-radius: 12px;
      padding: 1rem 2rem;
      box-shadow: var(--glass-shadow);
      z-index: 10000;
      animation: slideDown 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideUp 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 2000);
  }
}

// CSS for notification animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translate(-50%, -20px);
    }
    to {
      opacity: 1;
      transform: translate(-50%, 0);
    }
  }
  
  @keyframes themeTransition {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
  }
`;
document.head.appendChild(style);

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
  });
} else {
  window.themeManager = new ThemeManager();
}