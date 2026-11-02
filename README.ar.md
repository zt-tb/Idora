<div align="center" dir="rtl">

# Idora

**بوت تيليجرام يطلّع الشخص ومعلوماته عن طريق أيدي حساب تيليجرام.**

[English](README.md) · العربية

<a href="https://github.com/zt-tb/Idora/actions/workflows/checks.yml"><img src="https://github.com/zt-tb/Idora/actions/workflows/checks.yml/badge.svg" alt="Checks" /></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT%20%2B%20Attribution-2ea44f?style=flat" alt="License" /></a>
<img src="https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Telegram-Bot%20(Pyrogram%20fork)-26A5E4?logo=telegram&logoColor=white" alt="Telegram Bot" />
<img src="https://img.shields.io/badge/SQLite-database-003B57?logo=sqlite&logoColor=white" alt="SQLite" />
<img src="https://img.shields.io/badge/Payments-Telegram%20Stars-FFB400?logo=telegram&logoColor=white" alt="Telegram Stars" />
<img src="https://img.shields.io/badge/languages-Arabic%20%7C%20English-green" alt="Languages" />

<a href="https://t.me/K0_MG"><img src="https://img.shields.io/badge/Telegram-@K0__MG-26A5E4?logo=telegram&logoColor=white" alt="Telegram @K0_MG" /></a>
<a href="https://instagram.com/z0_28"><img src="https://img.shields.io/badge/Instagram-z0__28-E4405F?logo=instagram&logoColor=white" alt="Instagram z0_28" /></a>
<a href="https://www.tiktok.com/@zt_tb"><img src="https://img.shields.io/badge/TikTok-@zt__tb-000000?logo=tiktok&logoColor=white" alt="TikTok @zt_tb" /></a>
<a href="https://youtube.com/@M7JN"><img src="https://img.shields.io/badge/YouTube-@M7JN-FF0000?logo=youtube&logoColor=white" alt="YouTube @M7JN" /></a>
<a href="https://github.com/zt-tb"><img src="https://img.shields.io/badge/GitHub-zt--tb-181717?logo=github&logoColor=white" alt="GitHub zt-tb" /></a>

</div>

<div dir="rtl">

> **مفتوح المصدر مع ذكر الاسم.** Idora منشور برخصة MIT مع شرط ذكر الاسم. تقدر تستخدمه وتعدّل عليه وتشاركه، بشرط الاحتفاظ بملف [NOTICE](NOTICE) وترويسات الحقوق، وذكر المطوّر الأصلي **Mohsen Al-Taie (@K0_MG)**. التفاصيل بملف [LICENSE](LICENSE).

## شنو يسوي البوت

ترسل للبوت **أيدي** حساب تيليجرام. يرد عليك ببطاقة للحساب وستة أزرار، وكل زر يعطيك طريقة مختلفة لفتح حساب الشخص أو معرفة معلوماته.

كل شي يبدأ من الأيدي. إذا ما عندك الرقم، تكدر ترسل يوزر أو رسالة محوّلة أو جهة اتصال، والبوت يحوّلها للأيدي أول شي.

| الطريقة | شنو تحصل |
|---|---|
| 💬 **محادثة مباشرة** | زر يفتح محادثة ويا الحساب (`tg://openmessage?user_id=...`) |
| 👤 **الملف الشخصي** | زر يفتح الملف الشخصي (`tg://user?id=...`) |
| 🌐 **رابط اليوزر** | رابط `t.me/username` للحساب إذا عنده يوزر عام |
| 🖥 **تيليجرام ويب** | زر يفتح الحساب بتيليجرام ويب |
| 🔍 **معلومات الحساب** | الاسم واليوزر والبايو وعلامات مثل بريميوم أو بوت أو موثّق أو احتيال، إذا تيليجرام يظهرها للبوت |
| 🖼 **صورة الحساب** | صورة الحساب إذا عنده صورة يكدر البوت يشوفها |

المحادثة والملف الشخصي وتيليجرام ويب هي روابط تنفتح داخل تطبيق تيليجرام عندك. نجاحها يعتمد على تيليجرام: إذا تطبيقك ما شاف هذا الحساب قبل، ممكن الرابط ما يشتغل. وهذا سبب وجود زر **«❌ الرابط ما اشتغل»** (شرحه تحت).

## طريقة الاستخدام

1. افتح البوت بتيليجرام وأرسل `/start`.
2. أرسل **أيدي** الشخص الرقمي مثل `123456789` (الأرقام العربية والفارسية تشتغل أيضاً).
   - ما عندك الأيدي؟ هذي تنحوّل للأيدي تلقائياً: يوزر (`@username` أو رابط `t.me/username`)، أو رابط `tg://user?id=123456789`، أو رسالة **محوّلة** (Forward) من الشخص، أو **جهة اتصال** مشاركة.
3. اختار الطريقة من الأزرار تحت البطاقة.
4. تصلك النتيجة بالمحادثة، وتكدر تحفظ الحساب بالمفضلة باسم مستعار.

وتكدر تفتح بطاقة مباشرة: ضيف `?start=` وبعدها الأيدي لرابط البوت (مثلاً `?start=123456789`) وتنفتح بطاقة هذا الأيدي.

## التجربة المجانية والنجوم والاشتراك

- كل مستخدم عنده **تجربة مجانية واحدة**.
- بعدها كل عملية بـ**نجمة تيليجرام واحدة**، أو **اشتراك 30 يوم** بدون دفع لكل عملية.
- الدفع بنجوم تيليجرام (`XTR`) فما تحتاج مزوّد دفع.
- **العملية الي ما تطلع نتيجتها ما تنحسب.** إذا ما كو يوزر أو صورة أو معلومات، أو فشل الإرسال، ترجع التجربة المجانية أو ما تنخصم نجمة.
- زر **«❌ الرابط ما اشتغل»** يطلع تحت نتائج المحادثة والملف الشخصي وتيليجرام ويب. يرجّع التجربة المجانية أو يسترد النجمة تلقائياً، بحد أقصى 3 بلاغات لكل مستخدم، ويوصل إشعار للمطوّر.
- إذا فشل التسليم بعد الدفع، يُسترد المبلغ تلقائياً.
- المستخدم يكدر يضغط **طلب اشتراك**، فيوصل المطوّر إشعار بزر تفعيل.

## الأوامر

| الأمر | الوظيفة |
|---|---|
| `/start` | القائمة الرئيسية: أيدي حسابي، آخر أيدياتي، المفضلة، اشتراكي، طريقة الاستخدام، اللغة |
| `/help` | دليل الاستخدام |
| `/favs` | الحسابات المحفوظة بأسماء مستعارة (لحد 30) |
| `/plan` | تجربتك المجانية وسعر النجوم وحالة اشتراكك |
| `/lang` | التبديل بين العربي والإنجليزي |
| `/paysupport` | آخر مدفوعاتك وزر التواصل مع المطوّر |
| `/cancel` | إلغاء الخطوة الحالية |
| `/admin` | لوحة المطوّر (للمطوّر فقط) |
| `/refund USER_ID CHARGE_ID` | استرداد دفعة نجوم (للمطوّر فقط) |

اللغة تنختار تلقائياً من لغة تيليجرام عند المستخدم، وتتبدّل بأمر `/lang`.

## لوحة المطوّر

أمر `/admin` يفتح لوحة تشتغل فقط للحساب الموجود بـ`DEVELOPER_ID`:

- الإحصائيات وقائمة المشتركين وسجل العمليات وسجل كل مستخدم
- قائمة المدفوعات
- تفعيل أو إلغاء اشتراك (الافتراضي 30 يوم، أو `الأيدي عدد_الأيام`)
- إذاعة لكل المستخدمين مع معاينة وتأكيد وشريط تقدم
- حظر وفك حظر وعرض المحظورين

كل شي يتخزن بقاعدة بيانات SQLite محلية: المستخدمين والمفضلة والعمليات والتجارب المجانية والمدفوعات.

## التثبيت

**المتطلبات:** Python 3.11 أو أحدث، و`API_ID` و`API_HASH` من [my.telegram.org](https://my.telegram.org)، وتوكن بوت من [@BotFather](https://t.me/BotFather)، وأيدي حسابك.

| المتغير | مطلوب | الوصف |
|---|---|---|
| `API_ID` / `API_HASH` | نعم | من my.telegram.org |
| `BOT_TOKEN` | نعم | من @BotFather |
| `DEVELOPER_ID` | نعم | أيدي حسابك. الحساب الوحيد المسموح له بلوحة المطوّر |
| `DB_PATH` | لا | مسار قاعدة البيانات. الافتراضي `data/bot.db` |
| `TZ_OFFSET_HOURS` | لا | فرق التوقيت لعرض الأوقات. الافتراضي `3` |

التشغيل محلياً:

```bash
python -m venv .venv
source .venv/bin/activate        # على ويندوز: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # بعدها حط القيم الحقيقية داخل .env
python main.py
```

النشر على Railway:

1. ارفع المشروع إلى مستودع GitHub (لا ترفع `.env` أبداً).
2. بـRailway اختار **New Project ← Deploy from GitHub repo**.
3. ضيف `API_ID` و`API_HASH` و`BOT_TOKEN` و`DEVELOPER_ID` من **Variables**.
4. **مهم:** سوّي **Volume** وثبّته على `/app/data`، وخلي `DB_PATH=/app/data/bot.db`. بدونه تنمسح الاشتراكات والمدفوعات والسجلات عند كل نشر.
5. افتح الـLogs وتأكد من ظهور `Bot is starting`، بعدها أرسل `/start`.

## ملفات المشروع

| الملف | وظيفته |
|---|---|
| `main.py` | منطق البوت والدفع والمفضلة ولوحة المطوّر |
| `i18n.py` | كل نصوص المستخدم بالعربي والإنجليزي |
| `config.py` | قراءة الإعدادات من متغيرات البيئة |
| `Procfile` و`railway.json` و`runtime.txt` | إعدادات النشر (worker وPython 3.11) |

السعر (`STAR_PRICE`) والتجارب المجانية (`FREE_TRIALS`) ومدة الاشتراك (`SUB_DAYS`) والحدود كلها ثوابت بأول `main.py`.

## الخصوصية والأمان

Idora يعرض فقط الي يخلّي تيليجرام البوت يشوفه عن الحساب. ما يقرأ محادثات خاصة وما يكشف أرقام هواتف. استخدمه بمسؤولية واحترم خصوصية الناس. طريقة الإبلاغ عن ثغرة بملف [SECURITY.md](SECURITY.md). لا تشارك توكن البوت ولا `API_HASH` مع أحد.

## الحقوق

إذا استخدمت Idora أو بنيت عليه، اذكر المطوّر بالـREADME أو بوصف البوت، مثلاً: *Based on Idora by Mohsen Al-Taie (@K0_MG)*. وعند إعادة التوزيع لازم تبقى ملف `NOTICE`.

للاقتباس بالأبحاث أو التوثيق استخدم [CITATION.cff](CITATION.cff) (غيت هاب يعرض زر "Cite this repository").

## المطوّر

**Mohsen Al-Taie**

</div>

<div align="center">

<img src="assets/divider.svg" width="100%" alt="" />

### 📱 تابعني | Follow Me

<div dir="ltr">

<a href="https://t.me/K0_MG"><img src="assets/social/telegram.svg" width="72" alt="Telegram @K0_MG" /></a>
<a href="https://instagram.com/z0_28"><img src="assets/social/instagram.svg" width="72" alt="Instagram z0_28" /></a>
<a href="https://www.tiktok.com/@zt_tb"><img src="assets/social/tiktok.svg" width="72" alt="TikTok @zt_tb" /></a>
<a href="https://youtube.com/@M7JN"><img src="assets/social/youtube.svg" width="72" alt="YouTube @M7JN" /></a>
<a href="https://github.com/zt-tb"><img src="assets/social/github.svg" width="72" alt="GitHub zt-tb" /></a>

</div>

[تيليغرام @K0_MG](https://t.me/K0_MG) · [إنستغرام z0_28](https://instagram.com/z0_28) · [تيك توك @zt_tb](https://www.tiktok.com/@zt_tb) · [يوتيوب @M7JN](https://youtube.com/@M7JN) · [غيت هاب zt-tb](https://github.com/zt-tb)

<img src="assets/divider.svg" width="100%" alt="" />

</div>

<div align="center">

حقوق النشر (c) 2026 Mohsen Al-Taie (@K0_MG). انظر [LICENSE](LICENSE).

</div>
