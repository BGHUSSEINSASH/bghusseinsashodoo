# BGH ERP System - XML-RPC Server
# خادم XML-RPC للتكامل مع الأنظمة الخارجية (Odoo-style)

from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
import json

class XMLRPCHandler:
    """
    معالج XML-RPC على نمط Odoo للتكامل الخارجي
    """
    
    def __init__(self):
        self.authenticated_users = {}
    
    def authenticate(self, db, username, password):
        """
        مصادقة المستخدم وإرجاع UID
        """
        user = authenticate(username=username, password=password)
        if user:
            uid = user.id
            self.authenticated_users[uid] = user
            return uid
        return False
    
    def execute_kw(self, db, uid, password, model, method, args, kwargs=None):
        """
        تنفيذ عمليات على النماذج (ORM style)
        """
        if uid not in self.authenticated_users:
            return {'error': 'Not authenticated'}
        
        kwargs = kwargs or {}
        
        try:
            # Map model names to Django models
            model_map = {
                'res.partner': 'core.Customer',
                'product.product': 'core.Product',
                'account.invoice': 'accounting.Invoice',
                'sale.order': 'sales.SalesOrder',
                'purchase.order': 'purchases.PurchaseOrder',
                'stock.move': 'inventory.StockMove',
                'hr.employee': 'core.Employee',
                'hr.attendance': 'hr.Attendance',
                'project.project': 'project_management.Project',
                'project.task': 'project_management.Task',
            }
            
            django_model = model_map.get(model)
            if not django_model:
                return {'error': f'Model {model} not found'}
            
            # Execute method
            if method == 'search_read':
                return self._search_read(django_model, args, kwargs)
            elif method == 'create':
                return self._create(django_model, args, kwargs)
            elif method == 'write':
                return self._write(django_model, args, kwargs)
            elif method == 'unlink':
                return self._unlink(django_model, args, kwargs)
            elif method == 'read':
                return self._read(django_model, args, kwargs)
            else:
                return {'error': f'Method {method} not supported'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _search_read(self, model_name, args, kwargs):
        """
        البحث والقراءة
        """
        from django.apps import apps
        
        app_label, model = model_name.split('.')
        Model = apps.get_model(app_label, model)
        
        # Parse domain (simplified)
        domain = args[0] if args else []
        fields = kwargs.get('fields', [])
        limit = kwargs.get('limit', 100)
        offset = kwargs.get('offset', 0)
        
        queryset = Model.objects.all()
        
        # Apply filters from domain
        for condition in domain:
            if len(condition) == 3:
                field, operator, value = condition
                if operator == '=':
                    queryset = queryset.filter(**{field: value})
                elif operator == 'ilike':
                    queryset = queryset.filter(**{f'{field}__icontains': value})
        
        queryset = queryset[offset:offset + limit]
        
        # Serialize results
        results = []
        for obj in queryset:
            data = {'id': obj.id}
            for field in fields:
                if hasattr(obj, field):
                    value = getattr(obj, field)
                    # Handle foreign keys
                    if hasattr(value, 'id'):
                        data[field] = [value.id, str(value)]
                    else:
                        data[field] = str(value) if value else False
            results.append(data)
        
        return results
    
    def _create(self, model_name, args, kwargs):
        """
        إنشاء سجل جديد
        """
        from django.apps import apps
        
        app_label, model = model_name.split('.')
        Model = apps.get_model(app_label, model)
        
        values = args[0] if args else {}
        
        try:
            obj = Model.objects.create(**values)
            return obj.id
        except Exception as e:
            return {'error': str(e)}
    
    def _write(self, model_name, args, kwargs):
        """
        تحديث سجل
        """
        from django.apps import apps
        
        app_label, model = model_name.split('.')
        Model = apps.get_model(app_label, model)
        
        ids = args[0] if args else []
        values = args[1] if len(args) > 1 else {}
        
        try:
            Model.objects.filter(id__in=ids).update(**values)
            return True
        except Exception as e:
            return {'error': str(e)}
    
    def _unlink(self, model_name, args, kwargs):
        """
        حذف سجل
        """
        from django.apps import apps
        
        app_label, model = model_name.split('.')
        Model = apps.get_model(app_label, model)
        
        ids = args[0] if args else []
        
        try:
            Model.objects.filter(id__in=ids).delete()
            return True
        except Exception as e:
            return {'error': str(e)}
    
    def _read(self, model_name, args, kwargs):
        """
        قراءة سجلات محددة
        """
        from django.apps import apps
        
        app_label, model = model_name.split('.')
        Model = apps.get_model(app_label, model)
        
        ids = args[0] if args else []
        fields = kwargs.get('fields', [])
        
        try:
            objects = Model.objects.filter(id__in=ids)
            results = []
            
            for obj in objects:
                data = {'id': obj.id}
                for field in fields:
                    if hasattr(obj, field):
                        value = getattr(obj, field)
                        if hasattr(value, 'id'):
                            data[field] = [value.id, str(value)]
                        else:
                            data[field] = str(value) if value else False
                results.append(data)
            
            return results
        except Exception as e:
            return {'error': str(e)}


def start_xmlrpc_server(host='localhost', port=8069):
    """
    بدء خادم XML-RPC
    """
    handler = XMLRPCHandler()
    
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/xmlrpc/2/common', '/xmlrpc/2/object')
    
    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)
    server.register_introspection_functions()
    
    # Register methods
    server.register_function(handler.authenticate, 'authenticate')
    server.register_function(handler.execute_kw, 'execute_kw')
    
    print(f'🚀 XML-RPC Server running on {host}:{port}')
    print('Available endpoints:')
    print(f'  - http://{host}:{port}/xmlrpc/2/common')
    print(f'  - http://{host}:{port}/xmlrpc/2/object')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n👋 XML-RPC Server stopped')


# Django view for XML-RPC endpoint
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from xmlrpc.server import SimpleXMLRPCDispatcher

@csrf_exempt
def xmlrpc_endpoint(request):
    """
    نقطة نهاية XML-RPC في Django
    """
    if request.method == 'POST':
        dispatcher = SimpleXMLRPCDispatcher(allow_none=True, encoding=None)
        handler = XMLRPCHandler()
        
        dispatcher.register_function(handler.authenticate, 'authenticate')
        dispatcher.register_function(handler.execute_kw, 'execute_kw')
        
        response = dispatcher._marshaled_dispatch(
            request.body,
            lambda x: x
        )
        
        return HttpResponse(response, content_type='text/xml')
    else:
        return HttpResponse('XML-RPC Endpoint - POST requests only', status=405)


# Client usage example
"""
import xmlrpc.client

# Connect to server
url = 'http://localhost:8000/xmlrpc/2'
common = xmlrpc.client.ServerProxy(f'{url}/common')
models = xmlrpc.client.ServerProxy(f'{url}/object')

# Authenticate
db = 'bgh_erp'
username = 'admin'
password = 'admin'
uid = common.authenticate(db, username, password, {})

if uid:
    # Search and read customers
    customers = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_read',
        [[['customer', '=', True]]],
        {'fields': ['name', 'email', 'phone'], 'limit': 10}
    )
    print(customers)
    
    # Create new customer
    customer_id = models.execute_kw(
        db, uid, password,
        'res.partner', 'create',
        [{'name': 'New Customer', 'email': 'new@example.com'}]
    )
    print(f'Created customer ID: {customer_id}')
    
    # Update customer
    models.execute_kw(
        db, uid, password,
        'res.partner', 'write',
        [[customer_id], {'phone': '+1234567890'}]
    )
    
    # Delete customer
    models.execute_kw(
        db, uid, password,
        'res.partner', 'unlink',
        [[customer_id]]
    )
"""
