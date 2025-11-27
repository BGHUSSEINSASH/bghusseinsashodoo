// BGH ERP System - Main Application JavaScript
// نظام حسابات متكامل - التطبيق الرئيسي

class ERPSystem {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentModule = null;
        this.authToken = localStorage.getItem('auth_token');
        this.init();
    }

    init() {
        console.log('🚀 BGH ERP System initialized');
        this.setupEventListeners();
        this.loadDashboardData();
    }

    setupEventListeners() {
        // Navigation events
        document.addEventListener('DOMContentLoaded', () => {
            this.attachModuleListeners();
        });
    }

    attachModuleListeners() {
        const moduleButtons = document.querySelectorAll('[data-module]');
        moduleButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const module = e.target.dataset.module;
                this.loadModule(module);
            });
        });
    }

    // API Methods
    async apiRequest(endpoint, method = 'GET', data = null) {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }

        const config = {
            method,
            headers,
        };

        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}${endpoint}`, config);
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('API Error:', error);
            this.showNotification('حدث خطأ في الاتصال بالخادم', 'error');
            return null;
        }
    }

    // Dashboard Methods
    async loadDashboardData() {
        const stats = await this.getSystemStats();
        if (stats) {
            this.updateDashboard(stats);
        }
    }

    async getSystemStats() {
        // Fetch data from all modules
        const endpoints = [
            '/core/customers/',
            '/core/suppliers/',
            '/core/products/',
            '/accounting/invoices/',
            '/sales/orders/',
            '/purchases/orders/',
            '/hr/employees/'
        ];

        const results = {};
        for (const endpoint of endpoints) {
            const data = await this.apiRequest(endpoint);
            if (data) {
                const key = endpoint.split('/')[2];
                results[key] = Array.isArray(data) ? data.length : data.count || 0;
            }
        }
        return results;
    }

    updateDashboard(stats) {
        console.log('📊 Dashboard Stats:', stats);
        // Update UI with stats
        if (document.getElementById('total-customers')) {
            document.getElementById('total-customers').textContent = stats.customers || 0;
        }
        if (document.getElementById('total-products')) {
            document.getElementById('total-products').textContent = stats.products || 0;
        }
        if (document.getElementById('total-invoices')) {
            document.getElementById('total-invoices').textContent = stats.invoices || 0;
        }
    }

    // Module Management
    async loadModule(moduleName) {
        this.currentModule = moduleName;
        console.log(`📦 Loading module: ${moduleName}`);
        
        const moduleMap = {
            'customers': '/core/customers/',
            'suppliers': '/core/suppliers/',
            'products': '/core/products/',
            'invoices': '/accounting/invoices/',
            'sales': '/sales/orders/',
            'purchases': '/purchases/orders/',
            'inventory': '/inventory/moves/',
            'hr': '/hr/employees/'
        };

        const endpoint = moduleMap[moduleName];
        if (endpoint) {
            const data = await this.apiRequest(endpoint);
            this.renderModuleData(moduleName, data);
        }
    }

    renderModuleData(module, data) {
        const container = document.getElementById('module-content');
        if (!container) return;

        let html = `<div class="module-data">
            <h2>${this.getModuleTitle(module)}</h2>
            <div class="data-table">`;

        if (Array.isArray(data) && data.length > 0) {
            html += this.generateTable(data);
        } else if (data && data.results) {
            html += this.generateTable(data.results);
        } else {
            html += '<p>لا توجد بيانات متاحة</p>';
        }

        html += '</div></div>';
        container.innerHTML = html;
    }

    generateTable(data) {
        if (!data || data.length === 0) return '<p>لا توجد بيانات</p>';

        const headers = Object.keys(data[0]);
        let html = '<table class="data-table"><thead><tr>';
        
        headers.forEach(header => {
            html += `<th>${this.translateHeader(header)}</th>`;
        });
        html += '</tr></thead><tbody>';

        data.forEach(row => {
            html += '<tr>';
            headers.forEach(header => {
                html += `<td>${row[header] || '-'}</td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table>';
        return html;
    }

    getModuleTitle(module) {
        const titles = {
            'customers': '👥 العملاء',
            'suppliers': '📦 الموردين',
            'products': '🏷️ المنتجات',
            'invoices': '💰 الفواتير',
            'sales': '🛒 المبيعات',
            'purchases': '📥 المشتريات',
            'inventory': '📊 المخزون',
            'hr': '👔 الموارد البشرية'
        };
        return titles[module] || module;
    }

    translateHeader(header) {
        const translations = {
            'id': 'الرقم',
            'name': 'الاسم',
            'email': 'البريد الإلكتروني',
            'phone': 'الهاتف',
            'address': 'العنوان',
            'price': 'السعر',
            'quantity': 'الكمية',
            'status': 'الحالة',
            'date': 'التاريخ',
            'total': 'المجموع',
            'description': 'الوصف'
        };
        return translations[header] || header;
    }

    // CRUD Operations
    async createRecord(module, data) {
        const result = await this.apiRequest(`/${module}/`, 'POST', data);
        if (result) {
            this.showNotification('تم الحفظ بنجاح', 'success');
            this.loadModule(module);
        }
        return result;
    }

    async updateRecord(module, id, data) {
        const result = await this.apiRequest(`/${module}/${id}/`, 'PUT', data);
        if (result) {
            this.showNotification('تم التحديث بنجاح', 'success');
            this.loadModule(module);
        }
        return result;
    }

    async deleteRecord(module, id) {
        if (confirm('هل أنت متأكد من الحذف؟')) {
            const result = await this.apiRequest(`/${module}/${id}/`, 'DELETE');
            if (result !== null) {
                this.showNotification('تم الحذف بنجاح', 'success');
                this.loadModule(module);
            }
        }
    }

    // Utilities
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('ar-SA', {
            style: 'currency',
            currency: 'SAR'
        }).format(amount);
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('ar-SA').format(date);
    }

    exportToJSON(data, filename) {
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
    }

    exportToCSV(data, filename) {
        if (!data || data.length === 0) return;

        const headers = Object.keys(data[0]);
        const csv = [
            headers.join(','),
            ...data.map(row => headers.map(header => row[header]).join(','))
        ].join('\n');

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
    }
}

// Initialize the application
let erpSystem;
window.addEventListener('DOMContentLoaded', () => {
    erpSystem = new ERPSystem();
});

// WebSocket for real-time updates (if needed)
class ERPWebSocket {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => {
            console.log('🔌 WebSocket connected');
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('🔌 WebSocket disconnected');
            setTimeout(() => this.connect(), 5000);
        };
    }

    handleMessage(data) {
        console.log('📨 Received:', data);
        // Handle real-time updates
    }

    send(data) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ERPSystem, ERPWebSocket };
}
