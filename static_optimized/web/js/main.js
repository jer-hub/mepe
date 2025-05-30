/**
 * MEPE Cooperative - Main JavaScript File
 * Core functionality for the web application
 */

// Utility functions
const Utils = {
    // Local storage helpers
    storage: {
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (e) {
                console.warn('Failed to save to localStorage:', e);
            }
        },
        get: function(key) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : null;
            } catch (e) {
                console.warn('Failed to read from localStorage:', e);
                return null;
            }
        },
        remove: function(key) {
            try {
                localStorage.removeItem(key);
            } catch (e) {
                console.warn('Failed to remove from localStorage:', e);
            }
        }
    }
};

// Main Application Object
const CoopApp = {
    init: function() {
        this.initMobileMenu();
        console.log('MEPE Cooperative App initialized');
    },

    // Initialize mobile menu toggle
    initMobileMenu: function() {
        window.toggleMobileMenu = function() {
            const menu = document.getElementById('mobile-menu');
            if (menu) {
                menu.classList.toggle('hidden');
            }
        };
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    CoopApp.init();
});

// Export for use in other scripts
window.CoopApp = CoopApp;
window.Utils = Utils;
