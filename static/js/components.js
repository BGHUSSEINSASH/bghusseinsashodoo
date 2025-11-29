// BGH ERP System - OWL Component Framework
// نظام مكونات OWL (Odoo Web Library)

class ComponentManager {
    constructor() {
        this.components = new Map();
        this.activeComponent = null;
        this.eventBus = new EventTarget();
    }

    // Register a new component
    registerComponent(name, component) {
        this.components.set(name, component);
        console.log(`✅ Component registered: ${name}`);
    }

    // Mount component to DOM
    async mountComponent(name, target, props = {}) {
        const ComponentClass = this.components.get(name);
        if (!ComponentClass) {
            console.error(`❌ Component not found: ${name}`);
            return null;
        }

        const instance = new ComponentClass(props);
        instance.mount(target);
        this.activeComponent = instance;
        return instance;
    }

    // Emit event
    emit(eventName, detail) {
        this.eventBus.dispatchEvent(new CustomEvent(eventName, { detail }));
    }

    // Listen to event
    on(eventName, callback) {
        this.eventBus.addEventListener(eventName, callback);
    }
}

// Base Component Class (OWL-inspired)
class Component {
    constructor(props = {}) {
        this.props = props;
        this.state = this.initState();
        this.el = null;
        this.template = null;
    }

    initState() {
        return {};
    }

    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.render();
    }

    mount(target) {
        this.el = typeof target === 'string' ? document.querySelector(target) : target;
        if (this.el) {
            this.render();
            this.mounted();
        }
    }

    mounted() {
        // Hook called after component is mounted
    }

    willUnmount() {
        // Hook called before component is unmounted
    }

    render() {
        if (!this.el) return;
        const html = this.template ? this.template(this.state, this.props) : '';
        this.el.innerHTML = html;
        this.bindEvents();
    }

    bindEvents() {
        // Override to bind custom events
    }

    unmount() {
        this.willUnmount();
        if (this.el) {
            this.el.innerHTML = '';
        }
    }
}

// Customer List Component
class CustomerListComponent extends Component {
    initState() {
        return {
            customers: [],
            loading: true,
            searchTerm: ''
        };
    }

    async mounted() {
        await this.loadCustomers();
    }

    async loadCustomers() {
        try {
            const response = await fetch('/api/core/customers/');
            const data = await response.json();
            this.setState({ 
                customers: Array.isArray(data) ? data : data.results || [],
                loading: false 
            });
        } catch (error) {
            console.error('Error loading customers:', error);
            this.setState({ loading: false });
        }
    }

    template(state, props) {
        if (state.loading) {
            return '<div class="text-center p-5"><div class="spinner-border"></div></div>';
        }

        const filteredCustomers = state.customers.filter(c => 
            c.name?.toLowerCase().includes(state.searchTerm.toLowerCase())
        );

        return `
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0"><i class="bi bi-people-fill"></i> إدارة العملاء</h4>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <button class="btn btn-success" id="createCustomerBtn">
                                <i class="bi bi-plus-circle"></i> إضافة عميل جديد
                            </button>
                        </div>
                        <div class="col-md-6">
                            <input type="search" class="form-control" id="searchInput" 
                                placeholder="بحث عن عميل..." value="${state.searchTerm}">
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>الرقم</th>
                                    <th>الاسم</th>
                                    <th>البريد الإلكتروني</th>
                                    <th>الهاتف</th>
                                    <th>الإجراءات</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${filteredCustomers.map(customer => `
                                    <tr>
                                        <td>${customer.id}</td>
                                        <td>${customer.name || '-'}</td>
                                        <td>${customer.email || '-'}</td>
                                        <td>${customer.phone || '-'}</td>
                                        <td>
                                            <button class="btn btn-sm btn-primary edit-btn" data-id="${customer.id}">
                                                <i class="bi bi-pencil"></i>
                                            </button>
                                            <button class="btn btn-sm btn-danger delete-btn" data-id="${customer.id}">
                                                <i class="bi bi-trash"></i>
                                            </button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        const searchInput = this.el.querySelector('#searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.setState({ searchTerm: e.target.value });
            });
        }

        const createBtn = this.el.querySelector('#createCustomerBtn');
        if (createBtn) {
            createBtn.addEventListener('click', () => this.createCustomer());
        }

        this.el.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.currentTarget.dataset.id;
                this.editCustomer(id);
            });
        });

        this.el.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.currentTarget.dataset.id;
                this.deleteCustomer(id);
            });
        });
    }

    createCustomer() {
        const modal = new bootstrap.Modal(document.getElementById('createModal'));
        document.getElementById('modalContent').innerHTML = `
            <form id="customerForm">
                <div class="mb-3">
                    <label class="form-label">الاسم *</label>
                    <input type="text" class="form-control" name="name" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">البريد الإلكتروني *</label>
                    <input type="email" class="form-control" name="email" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">الهاتف</label>
                    <input type="text" class="form-control" name="phone">
                </div>
                <div class="mb-3">
                    <label class="form-label">العنوان</label>
                    <textarea class="form-control" name="address" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">حفظ</button>
            </form>
        `;
        
        document.getElementById('customerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                await fetch('/api/core/customers/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                modal.hide();
                this.loadCustomers();
                erpSystem.showNotification('تم إضافة العميل بنجاح', 'success');
            } catch (error) {
                erpSystem.showNotification('حدث خطأ', 'error');
            }
        });
        
        modal.show();
    }

    async editCustomer(id) {
        // Similar implementation
    }

    async deleteCustomer(id) {
        if (confirm('هل أنت متأكد من الحذف؟')) {
            try {
                await fetch(`/api/core/customers/${id}/`, { method: 'DELETE' });
                this.loadCustomers();
                erpSystem.showNotification('تم الحذف بنجاح', 'success');
            } catch (error) {
                erpSystem.showNotification('حدث خطأ', 'error');
            }
        }
    }
}

// Invoice List Component
class InvoiceListComponent extends Component {
    initState() {
        return {
            invoices: [],
            loading: true,
            statusFilter: ''
        };
    }

    async mounted() {
        await this.loadInvoices();
    }

    async loadInvoices() {
        try {
            const response = await fetch('/api/accounting/invoices/');
            const data = await response.json();
            this.setState({ 
                invoices: Array.isArray(data) ? data : data.results || [],
                loading: false 
            });
        } catch (error) {
            console.error('Error loading invoices:', error);
            this.setState({ loading: false });
        }
    }

    template(state, props) {
        if (state.loading) {
            return '<div class="text-center p-5"><div class="spinner-border"></div></div>';
        }

        const getStatusBadge = (status) => {
            const badges = {
                'draft': 'secondary',
                'posted': 'primary',
                'paid': 'success',
                'cancelled': 'danger'
            };
            return badges[status] || 'secondary';
        };

        const filteredInvoices = state.statusFilter 
            ? state.invoices.filter(inv => inv.status === state.statusFilter)
            : state.invoices;

        return `
            <div class="card shadow-sm">
                <div class="card-header bg-success text-white">
                    <h4 class="mb-0"><i class="bi bi-receipt"></i> إدارة الفواتير</h4>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <button class="btn btn-success" id="createInvoiceBtn">
                                <i class="bi bi-plus-circle"></i> فاتورة جديدة
                            </button>
                        </div>
                        <div class="col-md-6">
                            <select class="form-select" id="statusFilter">
                                <option value="">جميع الحالات</option>
                                <option value="draft">مسودة</option>
                                <option value="posted">منشورة</option>
                                <option value="paid">مدفوعة</option>
                                <option value="cancelled">ملغاة</option>
                            </select>
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead class="table-success">
                                <tr>
                                    <th>رقم الفاتورة</th>
                                    <th>العميل</th>
                                    <th>التاريخ</th>
                                    <th>المبلغ</th>
                                    <th>الحالة</th>
                                    <th>الإجراءات</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${filteredInvoices.map(invoice => `
                                    <tr>
                                        <td>${invoice.id}</td>
                                        <td>${invoice.customer || '-'}</td>
                                        <td>${invoice.date || '-'}</td>
                                        <td><span class="badge bg-info">${invoice.total || 0}</span></td>
                                        <td><span class="badge bg-${getStatusBadge(invoice.status)}">${invoice.status || '-'}</span></td>
                                        <td>
                                            <button class="btn btn-sm btn-info view-btn" data-id="${invoice.id}">
                                                <i class="bi bi-eye"></i>
                                            </button>
                                            <button class="btn btn-sm btn-primary edit-btn" data-id="${invoice.id}">
                                                <i class="bi bi-pencil"></i>
                                            </button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        const filterSelect = this.el.querySelector('#statusFilter');
        if (filterSelect) {
            filterSelect.addEventListener('change', (e) => {
                this.setState({ statusFilter: e.target.value });
            });
        }
    }
}

// Initialize Component Manager
const componentManager = new ComponentManager();

// Register all components
componentManager.registerComponent('customer-list', CustomerListComponent);
componentManager.registerComponent('invoice-list', InvoiceListComponent);

// Export for global use
window.componentManager = componentManager;
window.Component = Component;

console.log('🚀 OWL Component System initialized');
