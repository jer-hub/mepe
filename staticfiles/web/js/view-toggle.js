/**
 * View Toggle Functionality
 * Handles switching between table and card views
 */

const ViewToggle = {    init: function() {
        this.viewToggle = document.getElementById('viewToggle');
        this.tableView = document.getElementById('tableView');
        this.cardView = document.getElementById('cardView');
        this.viewText = document.getElementById('viewText');
        
        this.isTableView = true;
        this.storageKey = 'mepe-view-preference';
        
        if (this.viewToggle) {
            this.loadViewPreference();
            this.bindEvents();
        }
    },

    bindEvents: function() {
        this.viewToggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleView();
        });

        // Keyboard support
        this.viewToggle.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggleView();
            }
        });
    },

    toggleView: function() {
        if (this.isTableView) {
            this.switchToCardView();
        } else {
            this.switchToTableView();
        }
        this.saveViewPreference();
    },

    switchToCardView: function() {
        if (!this.tableView || !this.cardView) return;
        
        // Add transition classes
        this.tableView.style.transition = 'opacity 0.2s ease-out';
        this.cardView.style.transition = 'opacity 0.2s ease-in';
        
        // Fade out table
        this.tableView.style.opacity = '0';
        
        setTimeout(() => {
            this.tableView.classList.add('hidden');
            this.cardView.classList.remove('hidden');
            this.cardView.style.opacity = '0';
            
            // Fade in card view
            setTimeout(() => {
                this.cardView.style.opacity = '1';
            }, 50);        }, 200);

        // Update button state
        this.viewText.textContent = 'Cards';
        this.isTableView = false;

        // Update ARIA label
        this.viewToggle.setAttribute('aria-label', 'Switch to table view');
    },

    switchToTableView: function() {
        if (!this.tableView || !this.cardView) return;
        
        // Add transition classes
        this.cardView.style.transition = 'opacity 0.2s ease-out';
        this.tableView.style.transition = 'opacity 0.2s ease-in';
        
        // Fade out card
        this.cardView.style.opacity = '0';
        
        setTimeout(() => {
            this.cardView.classList.add('hidden');
            this.tableView.classList.remove('hidden');
            this.tableView.style.opacity = '0';
            
            // Fade in table view
            setTimeout(() => {
                this.tableView.style.opacity = '1';
            }, 50);        }, 200);

        // Update button state
        this.viewText.textContent = 'Table';
        this.isTableView = true;

        // Update ARIA label
        this.viewToggle.setAttribute('aria-label', 'Switch to card view');
    },

    saveViewPreference: function() {
        Utils.storage.set(this.storageKey, {
            isTableView: this.isTableView,
            timestamp: Date.now()
        });
    },

    loadViewPreference: function() {
        const preference = Utils.storage.get(this.storageKey);
        
        if (preference && preference.timestamp) {
            // Check if preference is less than 30 days old
            const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
            
            if (preference.timestamp > thirtyDaysAgo) {
                if (preference.isTableView === false) {
                    // User prefers card view
                    setTimeout(() => {
                        this.switchToCardView();
                    }, 100);
                }
            }
        }
    },

    // Public method to programmatically set view
    setView: function(viewType) {
        if (viewType === 'card' && this.isTableView) {
            this.switchToCardView();
            this.saveViewPreference();
        } else if (viewType === 'table' && !this.isTableView) {
            this.switchToTableView();
            this.saveViewPreference();
        }
    },

    // Get current view type
    getCurrentView: function() {
        return this.isTableView ? 'table' : 'card';
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    ViewToggle.init();
});

// Export for global access
window.ViewToggle = ViewToggle;
