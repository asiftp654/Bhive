class InvestmentManager {
    constructor() {
        this.selectedFund = null;
        this.investments = [];
        this.setupEventListeners();
    }

    setupEventListeners() {
        const investmentForm = document.getElementById('investmentForm');
        if (investmentForm) {
            investmentForm.addEventListener('submit', (e) => this.handleInvestment(e));
        }

        const unitsInput = document.getElementById('investmentUnits');
        if (unitsInput) {
            unitsInput.addEventListener('input', () => this.calculateInvestmentAmount());
        }
    }

    async searchMutualFunds() {
        const fundFamilySelect = document.getElementById('fundFamilySelect');
        const fundFamily = fundFamilySelect ? fundFamilySelect.value.trim() : '';

        if (!fundFamily) {
            showAlert('Please select a fund family to search.', 'error');
            return;
        }

        try {
            const funds = await api.searchMutualFunds(fundFamily);
            this.displaySearchResults(funds);
        } catch (error) {
            handleApiError(error);
        }
    }

    displaySearchResults(funds) {
        const searchResults = document.getElementById('searchResults');
        const fundsGrid = document.getElementById('fundsGrid');
        
        if (!funds || funds.length === 0) {
            searchResults.style.display = 'block';
            fundsGrid.innerHTML = `
                <div class="no-results">
                    <h3>No funds found</h3>
                    <p>Try searching with a different fund family name.</p>
                </div>
            `;
            return;
        }

        fundsGrid.innerHTML = funds.map(fund => this.createFundCardHTML(fund)).join('');
        searchResults.style.display = 'block';
    }

    createFundCardHTML(fund) {
        return `
            <div class="fund-card">
                <h4>${fund.Scheme_Name}</h4>
                <div class="fund-details">
                    <div class="fund-detail">
                        <span>Scheme Code:</span>
                        <span>${fund.Scheme_Code}</span>
                    </div>
                    <div class="fund-detail">
                        <span>Category:</span>
                        <span>${fund.Scheme_Category}</span>
                    </div>
                    <div class="fund-detail">
                        <span>NAV:</span>
                        <span>${formatCurrency(fund.Net_Asset_Value)}</span>
                    </div>
                </div>
                <button class="btn-primary" onclick="investmentManager.openInvestmentModal(${JSON.stringify(fund).replace(/"/g, '&quot;')})">
                    Invest
                </button>
            </div>
        `;
    }

    openInvestmentModal(fund) {
        this.selectedFund = fund;
        
        const fundDetailsEl = document.getElementById('selectedFundDetails');
        if (fundDetailsEl) {
            fundDetailsEl.innerHTML = `
                <div>
                    <h4>${fund.Scheme_Name}</h4>
                    <div class="fund-details">
                        <div class="fund-detail">
                            <span>Scheme Code:</span>
                            <span>${fund.Scheme_Code}</span>
                        </div>
                        <div class="fund-detail">
                            <span>Category:</span>
                            <span>${fund.Scheme_Category}</span>
                        </div>
                        <div class="fund-detail">
                            <span>Current NAV:</span>
                            <span>${formatCurrency(fund.Net_Asset_Value)}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        
        const navPerUnitEl = document.getElementById('navPerUnit');
        if (navPerUnitEl) {
            navPerUnitEl.textContent = formatCurrency(fund.Net_Asset_Value);
        }
        
        const unitsInput = document.getElementById('investmentUnits');
        if (unitsInput) {
            unitsInput.value = '';
        }
        this.calculateInvestmentAmount();
        
        const modal = document.getElementById('investmentModal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    closeInvestmentModal() {
        const modal = document.getElementById('investmentModal');
        if (modal) {
            modal.style.display = 'none';
        }
        
        const form = document.getElementById('investmentForm');
        if (form) {
            form.reset();
        }
        
        this.selectedFund = null;
    }

    calculateInvestmentAmount() {
        const unitsInput = document.getElementById('investmentUnits');
        const totalAmountEl = document.getElementById('totalInvestmentAmount');
        
        if (!unitsInput || !totalAmountEl || !this.selectedFund) {
            return;
        }
        
        const units = parseFloat(unitsInput.value) || 0;
        const nav = this.selectedFund.Net_Asset_Value || 0;
        const totalAmount = units * nav;
        
        totalAmountEl.textContent = formatCurrency(totalAmount);
    }

    async handleInvestment(event) {
        event.preventDefault();
        
        const units = parseInt(document.getElementById('investmentUnits').value);
        
        try {
            const investment = await api.createInvestment(this.selectedFund.Scheme_Code, units);
            
            showAlert(`Successfully invested in ${units} units of ${this.selectedFund.Scheme_Name}!`);
            this.closeInvestmentModal();
            
            authManager.loadPortfolioData();
        } catch (error) {
            handleApiError(error);
        }
    }

    displayInvestments(data) {
        const investments = data.investments || [];
        this.investments = investments;
        this.updateInvestmentsTable(investments);
    }

    updateInvestmentsTable(investments) {
        const tableBody = document.getElementById('investmentsTableBody');
        
        if (!tableBody) {
            return;
        }
        
        if (investments.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center">
                        <div class="no-investments">
                            <h3>No investments yet</h3>
                            <p>Start investing in mutual funds to see your portfolio here.</p>
                            <p>Use the search section below to find and invest in mutual funds.</p>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }
        
        tableBody.innerHTML = investments.map(investment => this.createInvestmentRowHTML(investment)).join('');
    }

    createInvestmentRowHTML(investment) {
        const profitLossClass = investment.profit_loss >= 0 ? 'profit' : 'loss';
        
        return `
            <tr>
                <td>
                    <div>
                        <strong>${investment.scheme_name}</strong>
                        <small>Code: ${investment.scheme_code}</small>
                    </div>
                </td>
                <td>${investment.units}</td>
                <td>${formatCurrency(investment.buy_price)}</td>
                <td>${formatCurrency(investment.current_price)}</td>
                <td class="${profitLossClass}">
                    ${formatCurrency(investment.profit_loss)}
                </td>
            </tr>
        `;
    }

    getInvestments() {
        return this.investments;
    }
}

const investmentManager = new InvestmentManager();

function searchMutualFunds() {
    investmentManager.searchMutualFunds();
}

function closeInvestmentModal() {
    investmentManager.closeInvestmentModal();
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { InvestmentManager, investmentManager };
}