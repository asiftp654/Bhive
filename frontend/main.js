document.addEventListener('DOMContentLoaded', () => {
    console.log('Bhive Mutual Fund App initialized');
    
    // Error handling
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled promise rejection:', event.reason);
        showAlert('An unexpected error occurred. Please refresh the page and try again.', 'error');
    });

    window.addEventListener('error', (event) => {
        console.error('JavaScript error:', event.error);
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            const modal = document.getElementById('investmentModal');
            if (modal) modal.style.display = 'none';
        }
        
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            const fundFamilySelect = document.getElementById('fundFamilySelect');
            if (fundFamilySelect) fundFamilySelect.focus();
        }
    });

    // Modal click outside to close
    document.addEventListener('click', (event) => {
        const modal = document.getElementById('investmentModal');
        if (modal && event.target === modal) {
            closeInvestmentModal();
        }
    });

    // Auto refresh portfolio every 5 minutes
    setInterval(() => {
        if (authManager.isLoggedIn()) {
            authManager.loadPortfolioData();
        }
    }, 5 * 60 * 1000);

    // Performance monitoring
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        console.log(`App loaded in ${loadTime.toFixed(2)}ms`);
    });
});

console.log('Bhive Mutual Fund Frontend loaded successfully!');