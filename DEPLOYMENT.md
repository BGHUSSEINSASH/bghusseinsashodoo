# دليل النشر - BGH ERP System

## 📌 الخطوات المطلوبة

### 1️⃣ رفع المشروع على GitHub

```powershell
# إنشاء repository جديد على GitHub أولاً من الموقع
# ثم قم بتنفيذ الأوامر التالية:

cd "c:\Users\BGHUSSEINSASH\Desktop\نظام حسابات متكامل"

# ربط المشروع بـ GitHub (استبدل USERNAME باسم المستخدم الخاص بك)
git remote add origin https://github.com/USERNAME/bgh-erp-system.git

# رفع المشروع
git branch -M main
git push -u origin main
```

### 2️⃣ النشر على Firebase

#### تثبيت Firebase CLI
```powershell
npm install -g firebase-tools
```

#### تسجيل الدخول
```powershell
firebase login
```

#### تهيئة المشروع
```powershell
cd "c:\Users\BGHUSSEINSASH\Desktop\نظام حسابات متكامل"
firebase init
```

اختر:
- ✅ Functions
- ✅ Hosting
- اختر مشروع Firebase موجود أو أنشئ جديد

#### النشر
```powershell
# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# النشر على Firebase
firebase deploy
```

### 3️⃣ النشر على Heroku (بديل)

#### تثبيت Heroku CLI
قم بتحميل وتثبيت من: https://devcenter.heroku.com/articles/heroku-cli

#### تسجيل الدخول وإنشاء التطبيق
```powershell
heroku login
heroku create bgh-erp-system
```

#### إضافة PostgreSQL Database
```powershell
heroku addons:create heroku-postgresql:hobby-dev
```

#### تعيين المتغيرات
```powershell
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="your-secret-key-here"
```

#### النشر
```powershell
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 4️⃣ فتح التطبيق
```powershell
# على Heroku
heroku open

# على Firebase
firebase open hosting:site
```

## 🔧 إعدادات إضافية

### متغيرات البيئة المطلوبة:
- `SECRET_KEY` - مفتاح Django السري
- `DEBUG` - False للإنتاج
- `DATABASE_URL` - رابط قاعدة البيانات (اختياري)
- `ALLOWED_HOSTS` - النطاقات المسموح بها

### قاعدة البيانات:
- Firebase: استخدم Cloud Firestore أو Cloud SQL
- Heroku: PostgreSQL (مضمّن)

## 📝 ملاحظات مهمة

1. ✅ تم إعداد Git repository محلياً
2. ⚠️ قم بإنشاء repository على GitHub يدوياً
3. ⚠️ قم بإنشاء مشروع Firebase من console.firebase.google.com
4. ⚠️ غيّر SECRET_KEY في الإنتاج
5. ⚠️ اضبط ALLOWED_HOSTS للنطاق الخاص بك

## 🌐 الروابط المفيدة

- GitHub: https://github.com
- Firebase Console: https://console.firebase.google.com
- Heroku Dashboard: https://dashboard.heroku.com

## 📞 الدعم

في حالة وجود مشاكل:
1. تحقق من logs: `heroku logs --tail` أو `firebase functions:log`
2. تأكد من تثبيت جميع المتطلبات: `pip install -r requirements.txt`
3. تأكد من تشغيل migrations: `python manage.py migrate`
