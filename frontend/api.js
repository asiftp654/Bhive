const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000'
    : 'http://localhost:8000';

class ApiService {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.token = localStorage.getItem('access_token');
    }

    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('access_token', token);
        } else {
            localStorage.removeItem('access_token');
        }
    }

    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (includeAuth && this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            headers: this.getHeaders(options.auth !== false),
            ...options,
        };

        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            showLoading(true);
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({
                    code: response.status,
                    message: response.statusText
                }));
                
                let errorMessage = 'An error occurred';
                if (errorData.message) {
                    if (typeof errorData.message === 'string') {
                        errorMessage = errorData.message;
                    } else if (Array.isArray(errorData.message)) {
                        errorMessage = errorData.message.map(err => {
                            if (typeof err === 'object') {
                                return Object.values(err)[0];
                            }
                            return err;
                        }).join(', ');
                    } else if (typeof errorData.message === 'object') {
                        errorMessage = Object.values(errorData.message)[0] || errorMessage;
                    }
                } else if (errorData.detail) {
                    errorMessage = errorData.detail;
                }
                
                throw new Error(errorMessage);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        } finally {
            showLoading(false);
        }
    }

    async get(endpoint, options = {}) {
        return this.request(endpoint, { method: 'GET', ...options });
    }

    async post(endpoint, data, options = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: data,
            ...options
        });
    }

    async signup(email, password) {
        return this.post('/users/signup', { email, password }, { auth: false });
    }

    async verifyOtp(email, otp) {
        if (!email) {
            throw new Error('Email is required for OTP verification');
        }
        
        if (!otp) {
            throw new Error('OTP is required for verification');
        }
        
        const response = await this.post('/users/verify-otp', { email, otp }, { auth: false });
        if (response.access_token) {
            this.setToken(response.access_token);
        }
        return response;
    }

    async login(email, password) {
        const response = await this.post('/users/login', { email, password }, { auth: false });
        if (response.access_token) {
            this.setToken(response.access_token);
        }
        return response;
    }

    async logout() {
        this.setToken(null);
        localStorage.removeItem('user_data');
    }

    async searchMutualFunds(fundFamily) {
        const params = new URLSearchParams({ fund_family: fundFamily });
        return this.get(`/mutual-funds?${params}`);
    }

    async getInvestments() {
        return this.get('/mutual-funds/investments');
    }

    async createInvestment(schemeCode, units) {
        return this.post('/mutual-funds/investments', {
            scheme_code: schemeCode,
            units: units
        });
    }

    isAuthenticated() {
        return !!this.token;
    }

    getUserData() {
        const userData = localStorage.getItem('user_data');
        return userData ? JSON.parse(userData) : null;
    }

    setUserData(userData) {
        localStorage.setItem('user_data', JSON.stringify(userData));
    }
}

const api = new ApiService();

function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = show ? 'flex' : 'none';
    }
}

function showAlert(message, type = 'success') {
    const alert = document.getElementById('alertMessage');
    const alertText = document.getElementById('alertText');
    
    if (alert && alertText) {
        alertText.textContent = message;
        alert.className = `alert ${type}`;
        alert.style.display = 'flex';
        
        setTimeout(() => {
            hideAlert();
        }, 5000);
    }
}

function hideAlert() {
    const alert = document.getElementById('alertMessage');
    if (alert) {
        alert.style.display = 'none';
    }
}

function handleApiError(error) {
    console.error('API Error:', error);
    
    let message = 'An unexpected error occurred. Please try again.';
    
    if (error.message) {
        message = error.message;
    }
    
    showAlert(message, 'error');
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { api, ApiService, showAlert, hideAlert, handleApiError, formatCurrency, formatDate };
}