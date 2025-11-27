# BGH ERP System - Webhooks Handler
# نظام حسابات متكامل - معالج الـ Webhooks

import json
import requests
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import datetime

class WebhookManager:
    """
    مدير الـ Webhooks للتفاعل مع الأنظمة الخارجية
    """
    
    def __init__(self):
        self.endpoints = getattr(settings, 'WEBHOOK_ENDPOINTS', {})
        self.enabled = getattr(settings, 'WEBHOOKS_ENABLED', True)
    
    def send_webhook(self, event_type, data):
        """
        إرسال webhook إلى النقاط المحددة
        """
        if not self.enabled:
            return
        
        webhook_url = self.endpoints.get(event_type)
        if not webhook_url:
            return
        
        payload = {
            'event': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Webhook sent successfully: {event_type}")
            else:
                print(f"❌ Webhook failed: {event_type} - Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Webhook error: {event_type} - {str(e)}")
    
    def prepare_data(self, instance):
        """
        تحضير البيانات للإرسال
        """
        data = {}
        for field in instance._meta.fields:
            value = getattr(instance, field.name)
            if hasattr(value, 'isoformat'):  # DateTime fields
                data[field.name] = value.isoformat()
            elif hasattr(value, 'pk'):  # ForeignKey fields
                data[field.name] = value.pk
            else:
                data[field.name] = str(value)
        return data


# Initialize webhook manager
webhook_manager = WebhookManager()


# Signal Handlers for Core Module
@receiver(post_save, sender='core.Customer')
def customer_webhook(sender, instance, created, **kwargs):
    """
    إرسال webhook عند إضافة أو تحديث عميل
    """
    event = 'customer.created' if created else 'customer.updated'
    data = webhook_manager.prepare_data(instance)
    webhook_manager.send_webhook(event, data)


@receiver(post_save, sender='core.Product')
def product_webhook(sender, instance, created, **kwargs):
    """
    إرسال webhook عند إضافة أو تحديث منتج
    """
    event = 'product.created' if created else 'product.updated'
    data = webhook_manager.prepare_data(instance)
    webhook_manager.send_webhook(event, data)


# Signal Handlers for Accounting Module
@receiver(post_save, sender='accounting.Invoice')
def invoice_webhook(sender, instance, created, **kwargs):
    """
    إرسال webhook عند إنشاء أو تحديث فاتورة
    """
    if created:
        event = 'invoice.created'
    elif instance.status == 'paid':
        event = 'invoice.paid'
    else:
        event = 'invoice.updated'
    
    data = webhook_manager.prepare_data(instance)
    webhook_manager.send_webhook(event, data)


# Signal Handlers for Sales Module
@receiver(post_save, sender='sales.SalesOrder')
def sales_order_webhook(sender, instance, created, **kwargs):
    """
    إرسال webhook عند إنشاء أو تحديث طلب بيع
    """
    if created:
        event = 'order.created'
    elif instance.status == 'delivered':
        event = 'order.delivered'
    elif instance.status == 'cancelled':
        event = 'order.cancelled'
    else:
        event = 'order.updated'
    
    data = webhook_manager.prepare_data(instance)
    webhook_manager.send_webhook(event, data)


# Signal Handlers for Inventory Module
@receiver(post_save, sender='inventory.StockMove')
def stock_move_webhook(sender, instance, created, **kwargs):
    """
    إرسال webhook عند حركة مخزون
    """
    event = 'stock.move'
    data = webhook_manager.prepare_data(instance)
    
    # Check if stock is low
    product = instance.product
    if hasattr(product, 'quantity') and product.quantity < 10:
        webhook_manager.send_webhook('stock.low', {
            'product_id': product.id,
            'product_name': product.name,
            'quantity': product.quantity,
            'warehouse': instance.warehouse.name if instance.warehouse else None
        })
    
    webhook_manager.send_webhook(event, data)


# External API Integrations
class ExternalAPIIntegration:
    """
    التكامل مع الأنظمة الخارجية
    """
    
    @staticmethod
    def sync_with_shopify(product_data):
        """
        مزامنة المنتجات مع Shopify
        """
        shopify_url = getattr(settings, 'SHOPIFY_API_URL', None)
        shopify_token = getattr(settings, 'SHOPIFY_API_TOKEN', None)
        
        if not shopify_url or not shopify_token:
            return None
        
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': shopify_token
        }
        
        try:
            response = requests.post(
                f"{shopify_url}/products.json",
                json={'product': product_data},
                headers=headers
            )
            return response.json()
        except Exception as e:
            print(f"Shopify sync error: {str(e)}")
            return None
    
    @staticmethod
    def process_paypal_payment(invoice_data):
        """
        معالجة الدفع عبر PayPal
        """
        paypal_url = getattr(settings, 'PAYPAL_API_URL', None)
        paypal_client_id = getattr(settings, 'PAYPAL_CLIENT_ID', None)
        
        if not paypal_url or not paypal_client_id:
            return None
        
        payment_data = {
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'transactions': [{
                'amount': {
                    'total': str(invoice_data.get('total')),
                    'currency': 'USD'
                },
                'description': invoice_data.get('description', 'Invoice payment')
            }]
        }
        
        try:
            response = requests.post(
                f"{paypal_url}/payments/payment",
                json=payment_data,
                auth=(paypal_client_id, getattr(settings, 'PAYPAL_SECRET', ''))
            )
            return response.json()
        except Exception as e:
            print(f"PayPal payment error: {str(e)}")
            return None
    
    @staticmethod
    def send_notification(channel, message):
        """
        إرسال إشعارات عبر قنوات مختلفة (Slack, Discord, etc.)
        """
        webhook_url = getattr(settings, f'{channel.upper()}_WEBHOOK_URL', None)
        
        if not webhook_url:
            return None
        
        payload = {'text': message} if channel.lower() == 'slack' else {'content': message}
        
        try:
            response = requests.post(webhook_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Notification error ({channel}): {str(e)}")
            return False


# REST API Utilities
class RESTAPIHelper:
    """
    مساعدات للتعامل مع REST API
    """
    
    @staticmethod
    def format_response(data, status='success', message=None):
        """
        تنسيق استجابة API موحدة
        """
        return {
            'status': status,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def paginate_response(queryset, page, page_size=20):
        """
        تقسيم النتائج إلى صفحات
        """
        start = (page - 1) * page_size
        end = start + page_size
        
        items = list(queryset[start:end])
        total = queryset.count()
        
        return {
            'items': items,
            'page': page,
            'page_size': page_size,
            'total': total,
            'pages': (total + page_size - 1) // page_size
        }
    
    @staticmethod
    def validate_json(data, required_fields):
        """
        التحقق من صحة بيانات JSON
        """
        errors = []
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"الحقل '{field}' مطلوب")
        
        return errors if errors else None


# GraphQL Schema (Optional)
"""
type Customer {
    id: ID!
    name: String!
    email: String!
    phone: String
    address: String
    createdAt: DateTime!
}

type Product {
    id: ID!
    name: String!
    price: Decimal!
    warehouse: Warehouse!
    description: String
}

type Query {
    customers: [Customer]
    customer(id: ID!): Customer
    products: [Product]
    product(id: ID!): Product
}

type Mutation {
    createCustomer(name: String!, email: String!): Customer
    updateCustomer(id: ID!, name: String, email: String): Customer
    deleteCustomer(id: ID!): Boolean
}
"""
