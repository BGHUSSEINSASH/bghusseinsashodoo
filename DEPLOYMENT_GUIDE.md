# BGH ERP System - دليل النشر والتشغيل

## نظرة عامة / Overview

نظام BGH ERP هو نظام محاسبة متكامل يعمل بالكامل على تقنيات الويب، تم بناؤه بأسلوب Odoo باستخدام أحدث التقنيات.

BGH ERP is a comprehensive accounting system built entirely with web technologies, following Odoo architecture using modern tech stack.

## التقنيات المستخدمة / Technology Stack

### Frontend
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with animations and transitions
- **Bootstrap 5 RTL**: Responsive framework with Arabic RTL support
- **Bootstrap Icons 1.11.2**: Icon library
- **JavaScript ES6+**: Modern JavaScript features
- **OWL-inspired Components**: Component-based architecture with lifecycle management
- **QWeb Templates**: XML-based templating system for dynamic UI rendering

### Backend
- **Python 3.13.9**: Modern Python version
- **Django 4.2.26**: Web framework
- **Django REST Framework 3.16.1**: API layer
- **Django ORM**: Database abstraction
- **XML-RPC Server**: Odoo-style external API integration

### Integration
- **REST API**: 50+ endpoints across 26 modules
- **XML-RPC**: External system integration (authenticate, execute_kw)
- **WebHooks**: Event-driven integrations (6 events)
- **JSON**: Data exchange format

### Deployment
- **GitHub**: https://github.com/BGHUSSEINSASH/bghusseinsashodoo
- **WhiteNoise**: Static file serving
- **Gunicorn-ready**: Production WSGI server support
- **Heroku/Railway-ready**: Cloud deployment configurations

## هيكل المشروع / Project Structure

```
نظام حسابات متكامل/
├── bgh_erp/                      # Django project settings
│   ├── settings.py               # Configuration (templates, static, APIs)
│   ├── urls.py                   # URL routing (homepage, API, XML-RPC)
│   └── wsgi.py                   # WSGI entry point
├── templates/
│   ├── base.html                 # Main HTML template with Bootstrap 5
│   └── api_docs.html             # API documentation page
├── static/
│   ├── css/
│   │   └── style.css             # Custom styles
│   ├── js/
│   │   ├── app.js                # Main application JavaScript
│   │   └── components.js         # OWL-inspired component framework
│   └── templates/
│       └── qweb_templates.xml    # QWeb component templates
├── api_views.py                  # API documentation views
├── xmlrpc_server.py              # XML-RPC server implementation
├── 26 Django Apps/               # All business modules
│   ├── core/                     # Customers, Products, Employees
│   ├── accounting/               # Invoices, Journal Entries
│   ├── sales/                    # Sales Orders, Quotations
│   ├── purchases/                # Purchase Orders
│   ├── inventory/                # Stock Management
│   ├── hr/                       # Human Resources
│   ├── projects/                 # Project Management
│   └── ... (21 more modules)
├── manage.py                     # Django management
└── requirements.txt              # Python dependencies
```

## الميزات الرئيسية / Key Features

### 1. Component Framework (إطار المكونات)
```javascript
// OWL-inspired component with lifecycle
class ComponentManager {
    static components = {};
    static register(name, componentClass) { ... }
    static mount(name, target, props) { ... }
}

class Component {
    initState() { ... }       // Initialize component state
    mounted() { ... }         // Component mounted to DOM
    willUnmount() { ... }     // Before unmounting
    render() { ... }          // Render component
    setState(updates) { ... } // Update state and re-render
}
```

### 2. QWeb Templates (قوالب QWeb)
```xml
<templates>
    <t t-name="core.customer_list">
        <div class="card">
            <div class="card-header">
                <h3>إدارة العملاء</h3>
            </div>
            <table class="table">
                <tbody>
                    <t t-foreach="customers" t-as="customer">
                        <tr>
                            <td t-esc="customer.name"/>
                            <td t-esc="customer.email"/>
                        </tr>
                    </t>
                </tbody>
            </table>
        </div>
    </t>
</templates>
```

### 3. XML-RPC API (واجهة XML-RPC)
```python
# Authenticate
uid = common.authenticate('bgh_erp', 'admin', 'password', {})

# Search and read customers
customers = models.execute_kw(
    'bgh_erp', uid, 'password',
    'res.partner', 'search_read',
    [[]], {'fields': ['name', 'email'], 'limit': 10}
)

# Create customer
customer_id = models.execute_kw(
    'bgh_erp', uid, 'password',
    'res.partner', 'create',
    [{'name': 'أحمد محمد', 'email': 'ahmed@example.com'}]
)
```

### 4. REST API Endpoints (نقاط نهاية REST)

**Core Module:**
- `GET /api/core/customers/` - List all customers
- `POST /api/core/customers/` - Create customer
- `GET /api/core/customers/{id}/` - Get customer
- `PUT /api/core/customers/{id}/` - Update customer
- `DELETE /api/core/customers/{id}/` - Delete customer

**Similar endpoints for:**
- Suppliers, Products, Warehouses, Employees
- Invoices, Journal Entries, Payments
- Sales Orders, Quotations
- Purchase Orders
- Inventory Moves, Stock Levels
- HR Attendance, Payrolls, Leaves
- Projects, Tasks, Timesheets
- Marketing Campaigns, Leads
- And 18 more modules...

## التثبيت والتشغيل / Installation & Setup

### 1. متطلبات النظام / System Requirements
```bash
Python 3.9+
pip (Python package manager)
Git
```

### 2. استنساخ المشروع / Clone Repository
```bash
git clone https://github.com/BGHUSSEINSASH/bghusseinsashodoo.git
cd bghusseinsashodoo
```

### 3. تثبيت المكتبات / Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. إعداد قاعدة البيانات / Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. جمع الملفات الثابتة / Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 6. تشغيل خادم التطوير / Run Development Server
```bash
python manage.py runserver
```

الوصول للنظام: http://127.0.0.1:8000/

## الصفحات الرئيسية / Main Pages

1. **الصفحة الرئيسية / Homepage**: http://127.0.0.1:8000/
   - لوحة المعلومات الرئيسية
   - إحصائيات النظام
   - النشاط الأخير

2. **توثيق API / API Documentation**: http://127.0.0.1:8000/api/docs/
   - جميع نقاط نهاية REST (50+ endpoints)
   - توثيق XML-RPC
   - أمثلة البرمجة (Python, JavaScript, cURL)
   - إرشادات المصادقة

3. **لوحة الإدارة / Admin Panel**: http://127.0.0.1:8000/admin/
   - إدارة البيانات
   - المستخدمين والصلاحيات
   - جميع النماذج (40+ models)

4. **فحص صحة النظام / Health Check**: http://127.0.0.1:8000/api/health/
   - حالة النظام
   - الإصدارات
   - الوحدات المتاحة

5. **معلومات النظام / System Info**: http://127.0.0.1:8000/api/info/
   - التقنيات المستخدمة
   - إحصائيات النظام

## المكونات المتاحة / Available Components

### مُطبّق / Implemented
1. **CustomerListComponent** - إدارة العملاء
   - عرض قائمة العملاء
   - البحث والتصفية
   - إضافة/تعديل/حذف عميل
   - نماذج Bootstrap Modal

2. **InvoiceListComponent** - إدارة الفواتير
   - عرض الفواتير
   - تصفية حسب الحالة
   - عرض التفاصيل

### قيد التطوير / In Development
- SalesOrderKanbanComponent (مبيعات)
- InventoryDashboardComponent (مخزون)
- AttendanceCalendarComponent (حضور)
- TaskBoardComponent (مشاريع)
- 20+ additional components for remaining modules

## نشر الإنتاج / Production Deployment

### خيار 1: Heroku
```bash
# Install Heroku CLI
heroku login
heroku create bgh-erp-system

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DJANGO_SETTINGS_MODULE=bgh_erp.settings
heroku config:set SECRET_KEY='your-secret-key'

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku open
```

### خيار 2: Railway
```bash
# Install Railway CLI
railway login
railway init

# Link PostgreSQL
railway add

# Deploy
railway up
```

### خيار 3: VPS (Ubuntu/Debian)
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup Gunicorn
pip install gunicorn
gunicorn bgh_erp.wsgi:application --bind 0.0.0.0:8000

# Configure Nginx
sudo nano /etc/nginx/sites-available/bgh_erp
# Add proxy configuration

# Enable and restart
sudo ln -s /etc/nginx/sites-available/bgh_erp /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## اختبار API / API Testing

### باستخدام cURL
```bash
# Get customers
curl http://127.0.0.1:8000/api/core/customers/

# Create customer
curl -X POST http://127.0.0.1:8000/api/core/customers/ \
  -H "Content-Type: application/json" \
  -d '{"name":"أحمد محمد","email":"ahmed@example.com"}'
```

### باستخدام Python
```python
import requests

base_url = 'http://127.0.0.1:8000/api'

# Get customers
response = requests.get(f'{base_url}/core/customers/')
customers = response.json()

# Create customer
new_customer = {
    'name': 'أحمد محمد',
    'email': 'ahmed@example.com'
}
response = requests.post(f'{base_url}/core/customers/', json=new_customer)
```

### باستخدام JavaScript (Fetch)
```javascript
// Get customers
const response = await fetch('/api/core/customers/');
const customers = await response.json();

// Create customer
await fetch('/api/core/customers/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'أحمد محمد',
        email: 'ahmed@example.com'
    })
});
```

## التطوير المستقبلي / Future Development

### المرحلة التالية / Next Phase
1. ✅ إكمال مكونات الـ 24 وحدة المتبقية
2. ✅ إضافة WebSocket للتحديثات الفورية
3. ✅ بناء تطبيق موبايل (React Native)
4. ✅ تحسين الأداء وإضافة Caching
5. ✅ إضافة اختبارات تلقائية (Unit Tests)
6. ✅ تحسين واجهة المستخدم
7. ✅ إضافة تقارير متقدمة
8. ✅ دعم لغات إضافية

## الدعم والمساعدة / Support

- **GitHub Issues**: https://github.com/BGHUSSEINSASH/bghusseinsashodoo/issues
- **Email**: bghusseinsash@example.com
- **Documentation**: http://127.0.0.1:8000/api/docs/

## الترخيص / License

MIT License - يمكن استخدامه تجارياً وشخصياً

---

**آخر تحديث / Last Updated**: نوفمبر 29, 2025  
**الإصدار / Version**: 1.0.0  
**المطور / Developer**: BGH Hussein Sash
