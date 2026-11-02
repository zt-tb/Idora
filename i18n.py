# Copyright (c) 2026 Mohsen Al-Taie (@K0_MG). See LICENSE (attribution required).
# -*- coding: utf-8 -*-

LINE = "━━━━━━━━━━━━━━━━━━"
LANGS = ("ar", "en")

METHOD_NAMES = {
    "chat": {"ar": "محادثة مباشرة", "en": "Direct chat"},
    "profile": {"ar": "الملف الشخصي", "en": "Profile"},
    "username": {"ar": "رابط اليوزر", "en": "Username link"},
    "web": {"ar": "تيليجرام ويب", "en": "Telegram Web"},
    "info": {"ar": "معلومات الحساب", "en": "Account info"},
    "photo": {"ar": "صورة الحساب", "en": "Profile photo"},
}

S = {
    "welcome": (
        "🌟 <b>هلا والله {name}</b> 🌟\n{line}\n"
        "💎 <b>بوت الروابط الذكية</b>\n\n"
        "أرسل لي واحد من هذي وأنا أسوّيلك الباقي 👇\n"
        "🔢 أيدي الحساب (مثل <code>123456789</code>)\n"
        "🏷 اليوزر (مثل <code>@username</code>)\n"
        "↪️ رسالة محوّلة من الشخص\n"
        "📇 جهة اتصال\n\n"
        "{status}",
        "🌟 <b>Welcome {name}</b> 🌟\n{line}\n"
        "💎 <b>Smart Link Bot</b>\n\n"
        "Send me any of these and I'll do the rest 👇\n"
        "🔢 A user ID (like <code>123456789</code>)\n"
        "🏷 A username (like <code>@username</code>)\n"
        "↪️ A message forwarded from the person\n"
        "📇 A shared contact\n\n"
        "{status}",
    ),
    "st_owner": ("👑 وضع المطور — كل شي مفتوح لك",
                 "👑 Developer mode — everything is unlocked"),
    "st_sub": ("💎 اشتراكك مفعّل — كل الطرق بلا حدود",
               "💎 Your plan is active — all methods, no limits"),
    "st_free": ("🎁 عندك <b>{free}</b> — وما تنحسب إذا ما طلعت النتيجة ✅",
                "🎁 You have <b>{free}</b> — not counted if there's no result ✅"),
    "st_nofree": ("⭐ <b>{price}</b> نجمة لكل عملية — وما تنحسب إذا ما طلعت النتيجة ✅",
                  "⭐ <b>{price}</b> Star per use — not charged if there's no result ✅"),
    "free_one": ("تجربة مجانية واحدة", "one free trial"),
    "free_n": ("{n} تجارب مجانية", "{n} free trials"),
    "free_avail": ("متاحة ✅", "available ✅"),
    "free_used": ("مستخدمة", "used"),
    "free_left_n": ("متبقي {left} من {n}", "{left} of {n} left"),

    "help": (
        "📖 <b>طريقة الاستخدام</b>\n{line}\n"
        "1️⃣ أرسل الأيدي <code>123456789</code> أو اليوزر <code>@username</code>\n"
        "    أو حوّل (Forward) أي رسالة من الشخص، أو شارك جهة اتصاله\n"
        "2️⃣ اختار الطريقة من الأزرار\n"
        "3️⃣ تصلك النتيجة فوراً\n\n"
        "🎁 عندك <b>{free}</b> فقط\n"
        "⭐ بعدها <b>{price}</b> نجمة لكل عملية، أو 💎 اشتراك شهري بلا حدود\n"
        "✅ إذا ما طلعت النتيجة ما ينحسب شي. وإذا انرسل الرابط وما اشتغل عندك "
        "اضغط «❌ الرابط ما اشتغل» ويرجعلك حقك.\n\n"
        "📌 <b>الأوامر:</b> /start • /favs • /plan • /lang • /help • /paysupport\n\n"
        "⚠️ <i>روابط المحادثة والملف والويب تشتغل بس إذا تطبيقك يعرف الشخص "
        "(تراسلتم قبل أو مجموعة مشتركة). المعلومات والصورة تعتمد على اللي يشوفه البوت.</i>",
        "📖 <b>How to use</b>\n{line}\n"
        "1️⃣ Send an ID <code>123456789</code> or a username <code>@username</code>\n"
        "    or forward any message from the person, or share their contact\n"
        "2️⃣ Pick a method from the buttons\n"
        "3️⃣ You get the result instantly\n\n"
        "🎁 You get <b>{free}</b> only\n"
        "⭐ After that, <b>{price}</b> Star per use, or a 💎 monthly plan with no limits\n"
        "✅ If there's no result, you're not charged. If a link was sent but didn't "
        "work for you, tap “❌ Link didn't work” and you get it back.\n\n"
        "📌 <b>Commands:</b> /start • /favs • /plan • /lang • /help • /paysupport\n\n"
        "⚠️ <i>Chat, profile and web links only open if your Telegram app already knows "
        "the person (past chat or a shared group). Info and photo depend on what the bot can see.</i>",
    ),

    "btn_myid": ("🆔 أيدي حسابي", "🆔 My ID"),
    "btn_recent": ("🕘 آخر أيدياتي", "🕘 Recent IDs"),
    "btn_favs": ("⭐ المفضلة", "⭐ Favorites"),
    "btn_plan": ("💎 اشتراكي", "💎 My plan"),
    "btn_help": ("📖 طريقة الاستخدام", "📖 How to use"),
    "btn_lang": ("🇬🇧 English", "🇮🇶 العربية"),
    "btn_admin": ("👑 لوحة التحكم", "👑 Admin panel"),
    "btn_home": ("🏠 الرئيسية", "🏠 Home"),
    "btn_back": ("🔙 رجوع", "🔙 Back"),
    "btn_save": ("⭐ حفظ بالمفضلة", "⭐ Save to favorites"),
    "btn_unsave": ("🗑 إزالة من المفضلة", "🗑 Remove from favorites"),
    "btn_favs_open": ("📂 المفضلة", "📂 Favorites"),
    "btn_prev": ("◀️ السابق", "◀️ Prev"),
    "btn_next": ("التالي ▶️", "Next ▶️"),
    "btn_pay": ("⭐ ادفع {price} نجمة", "⭐ Pay {price} Star"),
    "btn_subreq": ("💎 طلب اشتراك", "💎 Request plan"),
    "btn_subreq_long": ("📩 طلب اشتراك شهري", "📩 Request monthly plan"),
    "btn_bad": ("❌ الرابط ما اشتغل", "❌ Link didn't work"),
    "btn_yes_del": ("✅ نعم احذف", "✅ Yes, delete"),
    "btn_undo": ("↩️ تراجع", "↩️ Cancel"),
    "btn_dev": ("📩 تواصل مع المطور", "📩 Contact developer"),
    "open_chat": ("💬 فتح المحادثة", "💬 Open chat"),
    "open_profile": ("👤 فتح الملف الشخصي", "👤 Open profile"),
    "open_web": ("🖥 فتح في تيليجرام ويب", "🖥 Open in Telegram Web"),
    "open_username": ("🌐 فتح عبر اليوزر", "🌐 Open via username"),

    "card": (
        "✨ <b>تم استلام الأيدي</b> ✨\n{line}\n"
        "🆔 <b>الأيدي:</b> <code>{target}</code>\n{extra}{line}\n"
        "اختر طريقة الفتح 👇\n<i>{legend}</i>",
        "✨ <b>ID received</b> ✨\n{line}\n"
        "🆔 <b>ID:</b> <code>{target}</code>\n{extra}{line}\n"
        "Pick how to open it 👇\n<i>{legend}</i>",
    ),
    "card_alias": ("⭐ <b>محفوظ باسم:</b> {alias}\n", "⭐ <b>Saved as:</b> {alias}\n"),
    "via_fwd": ("↪️ من رسالة محوّلة\n", "↪️ From a forwarded message\n"),
    "via_contact": ("📇 من جهة اتصال\n", "📇 From a shared contact\n"),
    "via_user": ("🏷 من اليوزر {u}\n", "🏷 From username {u}\n"),
    "legend_owner": ("👑 وضع المطور — كل الطرق مفتوحة", "👑 Developer mode — all methods open"),
    "legend_sub": ("💎 اشتراكك مفعّل — كل الطرق مفتوحة", "💎 Your plan is active — all methods open"),
    "legend_free": ("🎁 عندك {free} — اختار أي طريقة وجرّبها مجاناً",
                    "🎁 You have {free} — pick any method and try it free"),
    "legend_pay": ("⭐ {price} نجمة للعملية • وما تنحسب إذا ما طلعت النتيجة",
                   "⭐ {price} Star per use • not charged if there's no result"),

    "fav_empty": (
        "⭐ <b>مفضلتك</b>\n{line}\n📭 القائمة فارغة حالياً.\nأرسل أيدي ثم اضغط <b>حفظ بالمفضلة</b>.",
        "⭐ <b>Your favorites</b>\n{line}\n📭 Nothing saved yet.\nSend an ID, then tap <b>Save to favorites</b>.",
    ),
    "fav_list": (
        "⭐ <b>مفضلتك</b> ({n}/{max})\n{line}\nاضغط على الاسم لفتح خيارات الأيدي 👇\n📄 صفحة {page}/{pages}",
        "⭐ <b>Your favorites</b> ({n}/{max})\n{line}\nTap a name to open its options 👇\n📄 Page {page}/{pages}",
    ),
    "recent_empty": (
        "🕘 <b>آخر أيدياتي</b>\n{line}\nما اكو شي بعد. أرسل أول أيدي وابدي 👌",
        "🕘 <b>Recent IDs</b>\n{line}\nNothing yet. Send your first ID to get started 👌",
    ),
    "recent_list": (
        "🕘 <b>آخر أيدياتي</b>\n{line}\nاضغط على أي واحد لفتح خياراته 👇",
        "🕘 <b>Recent IDs</b>\n{line}\nTap any one to open its options 👇",
    ),
    "alias_prompt": (
        "✏️ <b>أرسل الاسم المستعار</b> للأيدي <code>{target}</code>\n"
        "مثال: <i>أحمد - صديق</i>\n(لين 24 حرف • /cancel للإلغاء)",
        "✏️ <b>Send a nickname</b> for ID <code>{target}</code>\n"
        "Example: <i>Ahmed - friend</i>\n(up to 24 chars • /cancel to stop)",
    ),
    "alias_bad": ("⚠️ اكتب اسماً نصياً من 1 إلى 24 حرف (أو /cancel).",
                  "⚠️ Send a text name of 1–24 characters (or /cancel)."),
    "alias_saved": ("🎉 <b>تم الحفظ باسم:</b> {alias}", "🎉 <b>Saved as:</b> {alias}"),
    "fav_exists": ("⭐ هذا الأيدي محفوظ مسبقاً.", "⭐ Already in your favorites."),
    "fav_full": ("⚠️ وصلت الحد الأقصى ({max}). احذف بعضها أولاً.",
                 "⚠️ Limit reached ({max}). Delete some first."),
    "fav_missing": ("⚠️ غير موجود في المفضلة.", "⚠️ Not in your favorites."),
    "fav_del_confirm": ("🗑 <b>تأكيد الحذف</b>\n{line}\nحذف <code>{target}</code> من المفضلة؟",
                        "🗑 <b>Confirm delete</b>\n{line}\nRemove <code>{target}</code> from favorites?"),
    "fav_deleted": ("🗑 تم الحذف", "🗑 Deleted"),

    "plan": (
        "💎 <b>اشتراكك</b>\n{line}\n"
        "📌 الحالة: {status}\n"
        "🎁 التجربة المجانية: <b>{free}</b>\n"
        "⚙️ عملياتك: <b>{ops}</b>\n{line}\n"
        "• بعد التجربة المجانية: ⭐ <b>{price} نجمة</b> لكل عملية\n"
        "• أو 💎 اشتراك شهري بلا حدود يفعّله المطور\n"
        "• العملية اللي ما تطلع نتيجتها ما تنحسب ✅",
        "💎 <b>Your plan</b>\n{line}\n"
        "📌 Status: {status}\n"
        "🎁 Free trial: <b>{free}</b>\n"
        "⚙️ Your operations: <b>{ops}</b>\n{line}\n"
        "• After the free trial: ⭐ <b>{price} Star</b> per use\n"
        "• Or a 💎 monthly plan with no limits, activated by the developer\n"
        "• An operation with no result is never counted ✅",
    ),
    "plan_owner": ("👑 المطور — كل شي مفتوح", "👑 Developer — everything unlocked"),
    "plan_sub": ("✅ مفعّل لين <b>{date}</b> (باقي {days} يوم)",
                 "✅ Active until <b>{date}</b> ({days} days left)"),
    "plan_none": ("❌ غير مشترك", "❌ Not subscribed"),
    "subreq_have": ("💎 عندك وصول كامل أصلاً.", "💎 You already have full access."),
    "subreq_wait": ("⏳ طلبك مرسل من قبل، انتظر رد المطور.",
                    "⏳ Your request was already sent, please wait for the developer."),
    "subreq_sent": ("✅ انرسل طلبك للمطور، يوصلك إشعار لما يفعّله.",
                    "✅ Request sent to the developer — you'll be notified once it's activated."),
    "sub_activated": (
        "🎉 <b>تم تفعيل اشتراكك!</b>\n{line}\n💎 كل الطرق مفتوحة بلا حدود لين <b>{date}</b>\nاستمتع 🌹",
        "🎉 <b>Your plan is active!</b>\n{line}\n💎 All methods unlocked until <b>{date}</b>\nEnjoy 🌹",
    ),
    "sub_rejected": ("ℹ️ تعذر قبول طلب الاشتراك حالياً. تواصل مع المطور لمزيد من التفاصيل.",
                     "ℹ️ Your plan request couldn't be accepted right now. Contact the developer for details."),

    "paywall": (
        "🔒 <b>{method}</b>\n{line}\n"
        "خلصت تجربتك المجانية 🎁\n\n"
        "⭐ ادفع <b>{price} نجمة</b> لهذي العملية بس\n"
        "💎 أو اشترك شهرياً وافتح كل الطرق بلا حدود\n\n"
        "<i>إذا ما طلعت النتيجة ترجعلك النجمة تلقائياً ✅</i>",
        "🔒 <b>{method}</b>\n{line}\n"
        "Your free trial is used up 🎁\n\n"
        "⭐ Pay <b>{price} Star</b> for this one use\n"
        "💎 Or get a monthly plan and unlock every method\n\n"
        "<i>If there's no result, your Star is refunded automatically ✅</i>",
    ),
    "invoice_desc": ("{emoji} {name} للأيدي {target} — تصلك النتيجة فوراً بعد الدفع.",
                     "{emoji} {name} for ID {target} — you get the result right after payment."),
    "hint_link": (
        "\n\n💡 <i>الرابط يشتغل بس إذا تطبيقك يعرف الشخص (تراسلتم قبل أو مجموعة مشتركة).</i>",
        "\n\n💡 <i>The link only opens if your Telegram app already knows the person "
        "(past chat or a shared group).</i>",
    ),
    "hint_report": (
        "\n<i>إذا ما اشتغل اضغط «❌ الرابط ما اشتغل» وما ينحسب عليك.</i>",
        "\n<i>If it doesn't work, tap “❌ Link didn't work” and you won't be charged.</i>",
    ),
    "i_name": ("👤 <b>الاسم:</b> {v}", "👤 <b>Name:</b> {v}"),
    "i_user": ("🏷 <b>اليوزر:</b> @{v}", "🏷 <b>Username:</b> @{v}"),
    "i_bio": ("📝 <b>النبذة:</b> {v}", "📝 <b>Bio:</b> {v}"),
    "i_premium": ("💎 <b>بريميوم:</b> نعم", "💎 <b>Premium:</b> yes"),
    "i_bot": ("🤖 <b>النوع:</b> بوت", "🤖 <b>Type:</b> bot"),
    "i_verified": ("✅ <b>موثّق</b>", "✅ <b>Verified</b>"),
    "i_scam": ("⚠️ <b>مُعلَّم كاحتيال</b>", "⚠️ <b>Flagged as scam</b>"),
    "i_fake": ("🚫 <b>مُعلَّم كمزيّف</b>", "🚫 <b>Flagged as fake</b>"),
    "i_lang": ("🌐 <b>اللغة:</b> {v}", "🌐 <b>Language:</b> {v}"),
    "i_dc": ("🗄 <b>مركز البيانات:</b> DC{v}", "🗄 <b>Data center:</b> DC{v}"),

    "un_username": (
        "🏷 ما اكو يوزر معروف لهذا الحساب — ما انحسب شي ✅\nجرّب 💬 المحادثة أو 👤 الملف الشخصي.",
        "🏷 No known username for this account — nothing was counted ✅\nTry 💬 Direct chat or 👤 Profile.",
    ),
    "un_info": (
        "🔍 البوت ما يعرف هذا الحساب (ما تفاعل وياه) — ما انحسب شي ✅\nجرّب 💬 المحادثة أو 👤 الملف الشخصي.",
        "🔍 The bot doesn't know this account (no interaction) — nothing was counted ✅\n"
        "Try 💬 Direct chat or 👤 Profile.",
    ),
    "un_photo_none": ("🖼 ما اكو صورة متاحة لهذا الحساب — ما انحسب شي ✅",
                      "🖼 No photo is available for this account — nothing was counted ✅"),
    "un_photo_fail": ("🖼 تعذر جلب الصورة — ما انحسب شي ✅",
                      "🖼 Couldn't fetch the photo — nothing was counted ✅"),
    "un_unknown": ("طريقة غير معروفة.", "Unknown method."),

    "t_wait": ("⏳ لحظة...", "⏳ One moment..."),
    "t_err": ("⚠️ صار خطأ، حاول بعد شوي. (ما انحسب شي)",
              "⚠️ Something went wrong, try again shortly. (Nothing was counted)"),
    "t_send_fail": ("⚠️ تعذر الإرسال، جرّب مرة ثانية. (ما انحسب شي)",
                    "⚠️ Couldn't send, please try again. (Nothing was counted)"),
    "t_free_used": ("🎁 استخدمت تجربتك المجانية", "🎁 Free trial used"),
    "t_done": ("✅ تم", "✅ Done"),
    "t_invoice_fail": ("⚠️ تعذر إنشاء فاتورة الدفع الآن، حاول لاحقاً.",
                       "⚠️ Couldn't create the payment invoice, try again later."),
    "t_invalid": ("⚠️ طلب غير صالح.", "⚠️ Invalid request."),

    "co_invalid": ("طلب غير صالح.", "Invalid request."),
    "co_amount": ("مبلغ غير صحيح.", "Wrong amount."),
    "co_banned": ("حسابك محظور.", "Your account is banned."),
    "refund_auto": ("↩️ تعذر تنفيذ العملية، وتمت <b>إعادة نجمتك تلقائياً</b>.",
                    "↩️ We couldn't complete it, so your Star was <b>refunded automatically</b>."),
    "refund_dev": ("↩️ تمت <b>إعادة نجمتك</b> من المطور.", "↩️ Your Star was <b>refunded</b> by the developer."),
    "paysupport": (
        "🛟 <b>دعم المدفوعات</b>\n{line}\n"
        "إذا دفعت ولم تصلك النتيجة، أو واجهت أي مشكلة، تواصل مع المطور "
        "وأرسل له رقم العملية (charge) من القائمة أدناه.\n"
        "العمليات الفاشلة تُسترد تلقائياً قدر الإمكان.",
        "🛟 <b>Payment support</b>\n{line}\n"
        "If you paid and got no result, or hit any problem, contact the developer "
        "and send the charge ID from the list below.\n"
        "Failed operations are refunded automatically whenever possible.",
    ),
    "paysupport_mine": ("🧾 <b>آخر مدفوعاتك:</b>", "🧾 <b>Your latest payments:</b>"),

    "bad_done": ("ℹ️ سبق وبلّغت عن هذي العملية.", "ℹ️ You already reported this one."),
    "bad_nothing": ("ℹ️ هذي العملية ما انحسب عليها شي.", "ℹ️ Nothing was charged for this one."),
    "bad_limit": ("⚠️ وصلت حد البلاغات التلقائية. تواصل مع المطور وراح يراجعها.",
                  "⚠️ You've reached the automatic-report limit. Contact the developer to review it."),
    "bad_free_back": ("✅ رجعتلك تجربتك المجانية. جرّب طريقة ثانية 🙏",
                      "✅ Your free trial is back. Try another method 🙏"),
    "bad_star_back": ("✅ رجعتلك نجمتك تلقائياً.", "✅ Your Star was refunded automatically."),
    "bad_refund_failed": ("⚠️ تعذر الاسترداد التلقائي، تم إبلاغ المطور.",
                          "⚠️ Automatic refund failed — the developer was notified."),

    "nudge": (
        "🤔 ما فهمت المطلوب.\n{line}\nأرسل واحد من هذي:\n"
        "🔢 أيدي: <code>123456789</code>\n🏷 يوزر: <code>@username</code>\n"
        "↪️ رسالة محوّلة من الشخص\n📇 جهة اتصال\n\nأو اضغط زر من تحت 👇",
        "🤔 I didn't get that.\n{line}\nSend one of these:\n"
        "🔢 An ID: <code>123456789</code>\n🏷 A username: <code>@username</code>\n"
        "↪️ A message forwarded from the person\n📇 A shared contact\n\nOr tap a button below 👇",
    ),
    "err_not_text": ("⚠️ أرسل الأيدي نصاً، أو حوّل رسالة من الشخص، أو شارك جهة اتصاله.",
                     "⚠️ Send the ID as text, forward a message from the person, or share their contact."),
    "err_fwd": ("↪️ ما كدرت أطلع أيدي من هذي الرسالة (حساب الشخص مخفي أو مو شخص).\nجرّب تدز الأيدي أو اليوزر مباشرة.",
                "↪️ I couldn't read an ID from that message (the sender hides their account or isn't a person).\n"
                "Try sending the ID or username directly."),
    "err_contact": ("📇 جهة الاتصال هاي مو مربوطة بحساب تيليجرام.",
                    "📇 That contact isn't linked to a Telegram account."),
    "err_username": ("🏷 ما لگيت شخص باليوزر <code>@{u}</code>.\nتأكد من الكتابة (ممكن قناة أو مجموعة أو مو موجود).",
                     "🏷 I couldn't find a person with username <code>@{u}</code>.\n"
                     "Check the spelling (it may be a channel/group, or not exist)."),
    "err_chat_id": ("ℹ️ هذا أيدي مجموعة أو قناة، والبوت يشتغل مع أيديات الأشخاص بس.",
                    "ℹ️ That's a group/channel ID — I only work with people's IDs."),
    "err_many": ("🔢 لگيت أكثر من رقم بالرسالة. أرسل الأيدي لحاله.",
                 "🔢 I found more than one number. Please send just the ID."),
    "cooldown": ("⏳ مهلاً، انتظر ثانية بين كل طلب.", "⏳ Easy — wait a second between requests."),
    "duplicate": ("🔁 <b>سبق وأرسلت هذا الأيدي قبل لحظات</b>، شوف الرسالة اللي فوك.",
                  "🔁 <b>You just sent this ID</b> — see the message above."),

    "banned": ("🚫 <b>تم حظرك من استخدام البوت.</b>", "🚫 <b>You have been banned from using this bot.</b>"),
    "banned_cb": ("🚫 أنت محظور من استخدام البوت.", "🚫 You are banned from using this bot."),
    "cancel_ok": ("✅ تم إلغاء العملية.", "✅ Cancelled."),
    "cancel_none": ("ℹ️ ما اكو عملية جارية.", "ℹ️ Nothing to cancel."),
    "lang_pick": ("🌐 اختر اللغة • Choose language", "🌐 اختر اللغة • Choose language"),
    "lang_set": ("✅ تم تغيير اللغة إلى العربية 🇮🇶", "✅ Language changed to English 🇬🇧"),
    "my_id": ("🆔 هذا أيدي حسابك — اضغط عليه ينسخ 📋\n\n", "🆔 This is your account ID — tap it to copy 📋\n\n"),

    "cmd_start": ("الصفحة الرئيسية", "Main menu"),
    "cmd_help": ("طريقة الاستخدام", "How to use"),
    "cmd_favs": ("المفضلة", "Favorites"),
    "cmd_plan": ("اشتراكي وتجربتي المجانية", "My plan and free trial"),
    "cmd_lang": ("تغيير اللغة", "Change language"),
    "cmd_paysupport": ("دعم المدفوعات", "Payment support"),
}


def tr(lang: str, key: str, **kw) -> str:
    pair = S[key]
    text = pair[0] if lang == "ar" else pair[1]
    kw.setdefault("line", LINE)
    return text.format(**kw)


def free_phrase(lang: str, n: int) -> str:
    return tr(lang, "free_one") if n == 1 else tr(lang, "free_n", n=n)
