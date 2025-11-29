"""
BGH ERP API Documentation View
عرض توثيق REST API و XML-RPC
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

def api_documentation(request):
    """
    صفحة توثيق API الكاملة
    """
    api_endpoints = {
        'core': {
            'name': 'الأساسيات (Core)',
            'endpoints': [
                {'method': 'GET', 'url': '/api/core/customers/', 'description': 'عرض جميع العملاء'},
                {'method': 'POST', 'url': '/api/core/customers/', 'description': 'إضافة عميل جديد'},
                {'method': 'GET', 'url': '/api/core/customers/{id}/', 'description': 'عرض عميل محدد'},
                {'method': 'PUT', 'url': '/api/core/customers/{id}/', 'description': 'تحديث عميل'},
                {'method': 'DELETE', 'url': '/api/core/customers/{id}/', 'description': 'حذف عميل'},
                
                {'method': 'GET', 'url': '/api/core/suppliers/', 'description': 'عرض جميع الموردين'},
                {'method': 'POST', 'url': '/api/core/suppliers/', 'description': 'إضافة مورد جديد'},
                
                {'method': 'GET', 'url': '/api/core/products/', 'description': 'عرض جميع المنتجات'},
                {'method': 'POST', 'url': '/api/core/products/', 'description': 'إضافة منتج جديد'},
                
                {'method': 'GET', 'url': '/api/core/warehouses/', 'description': 'عرض جميع المستودعات'},
                {'method': 'GET', 'url': '/api/core/employees/', 'description': 'عرض جميع الموظفين'},
            ]
        },
        'accounting': {
            'name': 'المحاسبة (Accounting)',
            'endpoints': [
                {'method': 'GET', 'url': '/api/accounting/invoices/', 'description': 'عرض جميع الفواتير'},
                {'method': 'POST', 'url': '/api/accounting/invoices/', 'description': 'إنشاء فاتورة جديدة'},
                {'method': 'GET', 'url': '/api/accounting/expenses/', 'description': 'عرض المصروفات'},
            ]
        },
        'sales': {
            'name': 'المبيعات (Sales)',
            'endpoints': [
                {'method': 'GET', 'url': '/api/sales/orders/', 'description': 'عرض طلبات البيع'},
                {'method': 'POST', 'url': '/api/sales/orders/', 'description': 'إنشاء طلب بيع'},
                {'method': 'GET', 'url': '/api/sales/quotes/', 'description': 'عروض الأسعار'},
            ]
        },
        'purchases': {
            'name': 'المشتريات (Purchases)',
            'endpoints': [
                {'method': 'GET', 'url': '/api/purchases/orders/', 'description': 'عرض طلبات الشراء'},
                {'method': 'POST', 'url': '/api/purchases/orders/', 'description': 'إنشاء طلب شراء'},
            ]
        },
        'inventory': {
            'name': 'المخزون (Inventory)',
            'endpoints': [
                {'method': 'GET', 'url': '/api/inventory/moves/', 'description': 'حركات المخزون'},
                {'method': 'POST', 'url': '/api/inventory/moves/', 'description': 'تسجيل حركة'},
            ]
        },
        'hr': {
            'name': 'الموارد البشرية (HR)',
            'endpoints': [
                {'method': 'GET', 'url': '/api/hr/attendance/', 'description': 'سجلات الحضور'},
                {'method': 'POST', 'url': '/api/hr/attendance/', 'description': 'تسجيل حضور'},
                {'method': 'GET', 'url': '/api/hr/payrolls/', 'description': 'الرواتب'},
            ]
        },
        'projects': {
            'name': 'إدارة المشاريع (Projects)',
            'endpoints': [
                {'method': 'GET', 'url': '/api/projects/projects/', 'description': 'المشاريع'},
                {'method': 'GET', 'url': '/api/projects/tasks/', 'description': 'المهام'},
            ]
        },
        'marketing': {
            'name': 'التسويق (Marketing)',
            'endpoints': [
                {'method': 'GET', 'url': '/api/marketing/campaigns/', 'description': 'الحملات'},
                {'method': 'GET', 'url': '/api/marketing/leads/', 'description': 'العملاء المحتملين'},
            ]
        }
    }
    
    xmlrpc_info = {
        'endpoint': '/xmlrpc/2',
        'methods': [
            {
                'name': 'authenticate',
                'params': ['db', 'username', 'password'],
                'returns': 'uid or False',
                'description': 'مصادقة المستخدم'
            },
            {
                'name': 'execute_kw',
                'params': ['db', 'uid', 'password', 'model', 'method', 'args', 'kwargs'],
                'returns': 'result',
                'description': 'تنفيذ عمليات على النماذج'
            }
        ],
        'example': '''
import xmlrpc.client

url = 'http://localhost:8000/xmlrpc/2'
common = xmlrpc.client.ServerProxy(f'{url}/common')
models = xmlrpc.client.ServerProxy(f'{url}/object')

# Authenticate
uid = common.authenticate('bgh_erp', 'admin', 'password', {})

# Search customers
customers = models.execute_kw(
    'bgh_erp', uid, 'password',
    'res.partner', 'search_read',
    [[]], {'fields': ['name', 'email'], 'limit': 10}
)
        '''
    }
    
    context = {
        'api_endpoints': api_endpoints,
        'xmlrpc_info': xmlrpc_info,
        'total_endpoints': sum(len(module['endpoints']) for module in api_endpoints.values())
    }
    
    return render(request, 'api_docs.html', context)


@api_view(['GET'])
def api_health_check(request):
    """
    فحص صحة API
    """
    return Response({
        'status': 'healthy',
        'version': '1.0.0',
        'endpoints': {
            'rest_api': '/api/',
            'xmlrpc': '/xmlrpc/2',
            'documentation': '/api/docs/',
            'admin': '/admin/'
        },
        'modules': [
            'core', 'accounting', 'sales', 'purchases', 'inventory',
            'hr', 'projects', 'marketing', 'website', 'pos',
            'manufacturing', 'maintenance', 'documents', 'subscriptions',
            'fleet', 'quality', 'helpdesk', 'events', 'elearning',
            'recruitment', 'sign', 'email_marketing', 'surveys',
            'appointments', 'expenses', 'discuss'
        ]
    })


@api_view(['GET'])
def system_info(request):
    """
    معلومات النظام
    """
    import django
    import sys
    
    return Response({
        'system': 'BGH ERP System',
        'version': '1.0.0',
        'python_version': sys.version,
        'django_version': django.get_version(),
        'technologies': {
            'frontend': ['HTML5', 'CSS3', 'JavaScript', 'Bootstrap 5', 'QWeb', 'OWL Components'],
            'backend': ['Python', 'Django', 'Django REST Framework', 'Django ORM'],
            'integrations': ['REST API', 'XML-RPC', 'Webhooks', 'JSON'],
            'deployment': ['Firebase', 'GitHub', 'Heroku-ready']
        },
        'statistics': {
            'modules': 26,
            'models': '40+',
            'api_endpoints': '50+',
            'webhooks': 6
        }
    })
