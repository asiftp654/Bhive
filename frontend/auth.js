class AuthManager {
    constructor() {
        this.currentUser = null;
        this.pendingVerificationEmail = null;
        this.init();
    }

    init() {
        if (api.isAuthenticated()) {
            const userData = api.getUserData();
            if (userData) {
                this.currentUser = userData;
                this.showMainApp();
            } else {
                this.showAuthSection();
            }
        } else {
            this.showAuthSection();
        }
        this.setupEventListeners();
    }

    setupEventListeners() {
        ['loginForm', 'signupForm', 'otpForm'].forEach((formId, index) => {
            const form = document.getElementById(formId);
            if (form) {
                const handlers = [
                    (e) => this.handleLogin(e),
                    (e) => this.handleSignup(e),
                    (e) => this.handleOtpVerification(e)
                ];
                form.addEventListener('submit', handlers[index]);
            }
        });
    }

    async handleLogin(event) {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await api.login(email, password);
            api.setUserData(response.user);
            this.currentUser = response.user;
            showAlert(`Welcome back, ${response.user.name || response.user.email}!`);
            this.showMainApp();
        } catch (error) {
            handleApiError(error);
        }
    }

    async handleSignup(event) {
        event.preventDefault();
        const email = document.getElementById('signupEmail').value.trim();
        const password = document.getElementById('signupPassword').value;

        try {
            const response = await api.signup(email, password);
            this.pendingVerificationEmail = email;
            showAlert(response.message);
            this.showOtpForm(email);
        } catch (error) {
            handleApiError(error);
        }
    }

    async handleOtpVerification(event) {
        event.preventDefault();
        
        let email = this.pendingVerificationEmail || document.getElementById('otpEmail').textContent.trim();
        const otpInput = document.getElementById('otpCode').value.trim();
        
        if (!email) {
            showAlert('Email not found. Please try signing up again.', 'error');
            this.showSignupForm();
            return;
        }
        
        if (!otpInput || otpInput.length !== 6) {
            showAlert('Please enter a valid 6-digit OTP code.', 'error');
            return;
        }
        
        const otp = parseInt(otpInput);
        if (isNaN(otp)) {
            showAlert('OTP must be a valid number.', 'error');
            return;
        }

        try {
            const response = await api.verifyOtp(email, otp);
            this.pendingVerificationEmail = null;
            api.setUserData(response.user);
            this.currentUser = response.user;
            showAlert(`Account verified successfully! Welcome, ${response.user.name || response.user.email}!`);
            this.showMainApp();
        } catch (error) {
            handleApiError(error);
        }
    }

    showAuthSection() {
        this.toggleDisplay('authSection', 'flex', 'mainApp', 'none');
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) logoutBtn.style.display = 'none';
    }

    showMainApp() {
        this.toggleDisplay('authSection', 'none', 'mainApp', 'block');
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) logoutBtn.style.display = 'block';
        
        this.loadPortfolioData();
        this.populateFundFamilyDropdown();
    }

    toggleDisplay(hideId, hideValue, showId, showValue) {
        document.getElementById(hideId).style.display = hideValue;
        document.getElementById(showId).style.display = showValue;
    }

    showLoginForm() {
        this.switchForm('loginForm', 'Welcome Back');
    }

    showSignupForm() {
        this.switchForm('signupForm', 'Create Account');
    }

    showOtpForm(email) {
        this.switchForm('otpForm', 'Verify Email');
        document.getElementById('otpEmail').textContent = email;
        document.getElementById('otpCode').value = '';
    }

    switchForm(activeForm, title) {
        ['loginForm', 'signupForm', 'otpForm'].forEach(form => {
            document.getElementById(form).style.display = form === activeForm ? 'block' : 'none';
        });
        document.getElementById('authTitle').textContent = title;
        this.clearForms();
    }

    clearForms() {
        ['loginForm', 'signupForm', 'otpForm'].forEach(formId => {
            const form = document.getElementById(formId);
            if (form) form.reset();
        });
        this.pendingVerificationEmail = null;
    }

    async logout() {
        try {
            await api.logout();
            this.currentUser = null;
            showAlert('Logged out successfully!');
            this.showAuthSection();
            this.showLoginForm();
        } catch (error) {
            console.error('Logout error:', error);
            api.logout();
            this.currentUser = null;
            this.showAuthSection();
            this.showLoginForm();
        }
    }

    async loadPortfolioData() {
        try {
            const investmentsData = await api.getInvestments();
            this.updatePortfolioStats(investmentsData);
            investmentManager.displayInvestments(investmentsData);
        } catch (error) {
            console.error('Error loading portfolio data:', error);
        }
    }

    async reloadPortfolio() {
        const reloadBtn = document.getElementById('reloadBtn');
        if (reloadBtn) {
            reloadBtn.disabled = true;
            reloadBtn.textContent = 'Updating...';
        }

        try {
            showAlert('Refreshing portfolio data...', 'info');
            const investmentsData = await api.getInvestments();
            this.updatePortfolioStats(investmentsData);
            investmentManager.displayInvestments(investmentsData);
            showAlert('Portfolio refreshed successfully!');
        } catch (error) {
            console.error('Error reloading portfolio:', error);
            handleApiError(error);
        } finally {
            if (reloadBtn) {
                reloadBtn.disabled = false;
                reloadBtn.textContent = 'Reload Prices';
            }
        }
    }

    updatePortfolioStats(data) {
        const investments = data.investments || [];
        const totalProfitLoss = data.total_profit_loss || 0;
        
        let totalInvestmentValue = 0;
        let currentValue = 0;
        
        investments.forEach(investment => {
            totalInvestmentValue += investment.buy_price * investment.units;
            currentValue += investment.current_price * investment.units;
        });
        
        const elements = {
            totalInvestments: formatCurrency(totalInvestmentValue),
            portfolioValue: formatCurrency(currentValue),
            totalProfitLoss: formatCurrency(totalProfitLoss),
            totalFunds: investments.length
        };
        
        Object.keys(elements).forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.textContent = elements[id];
                if (id === 'totalProfitLoss') {
                    el.className = totalProfitLoss >= 0 ? 'profit' : 'loss';
                }
            }
        });
    }

    populateFundFamilyDropdown() {
        const fundFamilySelect = document.getElementById('fundFamilySelect');
        if (!fundFamilySelect) return;

        const mutualFundFamilies = [
            "Navi Mutual Fund", "SBI Mutual Fund", "Tata Mutual Fund", "Edelweiss Mutual Fund",
            "Bank of India Mutual Fund", "LIC Mutual Fund", "Sundaram Mutual Fund", "quant Mutual Fund",
            "Bandhan Mutual Fund", "DSP Mutual Fund", "Quantum Mutual Fund", "Angel One Mutual Fund",
            "Taurus Mutual Fund", "Jio BlackRock Mutual Fund", "Old Bridge Mutual Fund", "Baroda BNP Paribas Mutual Fund",
            "JM Financial Mutual Fund", "Canara Robeco Mutual Fund", "Bajaj Finserv Mutual Fund", "HDFC Mutual Fund",
            "HSBC Mutual Fund", "Invesco Mutual Fund", "Capitalmind Mutual Fund", "Trust Mutual Fund",
            "360 ONE Mutual Fund", "NJ Mutual Fund", "Mahindra Manulife Mutual Fund", "Groww Mutual Fund",
            "Zerodha Mutual Fund", "UTI Mutual Fund", "Unifi Mutual Fund", "ICICI Prudential Mutual Fund",
            "Franklin Templeton Mutual Fund", "PPFAS Mutual Fund", "WhiteOak Capital Mutual Fund", "Motilal Oswal Mutual Fund",
            "Shriram Mutual Fund", "Aditya Birla Sun Life Mutual Fund", "Kotak Mahindra Mutual Fund", "Samco Mutual Fund",
            "Helios Mutual Fund", "Mirae Asset Mutual Fund", "ITI Mutual Fund", "PGIM India Mutual Fund",
            "Nippon India Mutual Fund", "Axis Mutual Fund", "Union Mutual Fund"
        ];

        fundFamilySelect.innerHTML = '<option value="">Choose a fund family...</option>' + 
            mutualFundFamilies.map(family => `<option value="${family}">${family}</option>`).join('');
    }

    getCurrentUser() {
        return this.currentUser;
    }

    isLoggedIn() {
        return !!this.currentUser && api.isAuthenticated();
    }
}

const authManager = new AuthManager();

function showLoginForm() {
    authManager.showLoginForm();
}

function showSignupForm() {
    authManager.showSignupForm();
}

function logout() {
    authManager.logout();
}

function reloadPortfolio() {
    authManager.reloadPortfolio();
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AuthManager, authManager };
}