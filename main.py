# Copyright (c) 2026 Mohsen Al-Taie (@K0_MG). See LICENSE (attribution required).
# -*- coding: utf-8 -*-

import asyncio
import html
import logging
import os
import re
import sqlite3
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from config import API_HASH, API_ID, BOT_TOKEN, DB_PATH, DEVELOPER_ID, TZ_OFFSET
from i18n import LINE, METHOD_NAMES, free_phrase, tr
from pyrogram import Client, StopPropagation, filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, InputUserDeactivated, PeerIdInvalid, UserIsBlocked
from pyrogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    Message,
)

try:
    from pyrogram.enums import ButtonStyle
    STYLES_OK = True
except ImportError:
    ButtonStyle = None
    STYLES_OK = False

OWNER_ID = DEVELOPER_ID

os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
FREE_TRIALS = 1
MAX_REPORTS = 3
MAX_FAVS = 30
FAVS_PER_PAGE = 6
RECENT_LIMIT = 6
REQUEST_COOLDOWN = 1.5
DUPLICATE_WINDOW = 10
STAR_PRICE = 1
SUB_DAYS = 30
SUBREQ_COOLDOWN = 600
START_TIME = time.time()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("linkbot")

app = Client(
    "linkbot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML,
)

METHODS = {
    "chat": "💬",
    "profile": "👤",
    "username": "🌐",
    "web": "🖥",
    "info": "🔍",
    "photo": "🖼",
}
LINK_METHODS = {"chat", "profile", "web"}
METHOD_STYLE = {
    "chat": "PRIMARY", "profile": "SUCCESS", "username": "PRIMARY",
    "web": "SUCCESS", "info": "PRIMARY", "photo": "SUCCESS",
}
KIND_ICON = {"free": "🎁", "paid": "⭐", "sub": "💎", "owner": "👑", "legacy": "📦"}
COMMANDS = ["start", "help", "favs", "cancel", "admin", "plan", "paysupport", "refund", "lang"]

_db = sqlite3.connect(DB_PATH, check_same_thread=False)
_db.row_factory = sqlite3.Row
_lock = threading.Lock()


def db_exec(sql, params=(), fetch=None):
    with _lock:
        cur = _db.execute(sql, params)
        _db.commit()
        if fetch == "one":
            return cur.fetchone()
        if fetch == "all":
            return cur.fetchall()
        return cur


with _lock:
    _db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY, name TEXT, username TEXT,
            joined INTEGER, banned INTEGER DEFAULT 0, sub_until INTEGER DEFAULT 0,
            lang TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS favorites(
            owner INTEGER, target INTEGER, alias TEXT, created INTEGER,
            PRIMARY KEY(owner, target));
        CREATE TABLE IF NOT EXISTS operations(
            id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER, user_id INTEGER,
            target INTEGER, method TEXT, kind TEXT,
            ref TEXT DEFAULT '', refunded INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS free_used(
            user_id INTEGER, method TEXT, ts INTEGER,
            PRIMARY KEY(user_id, method));
        CREATE TABLE IF NOT EXISTS free_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, method TEXT, ts INTEGER);
        CREATE INDEX IF NOT EXISTS idx_free_log_user ON free_log(user_id);
        CREATE TABLE IF NOT EXISTS payments(
            charge_id TEXT PRIMARY KEY, user_id INTEGER, target INTEGER,
            method TEXT, stars INTEGER, ts INTEGER, status TEXT);
        """
    )
    for _ddl in (
        "ALTER TABLE users ADD COLUMN sub_until INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN lang TEXT DEFAULT ''",
        "ALTER TABLE operations ADD COLUMN ref TEXT DEFAULT ''",
        "ALTER TABLE operations ADD COLUMN refunded INTEGER DEFAULT 0",
    ):
        try:
            _db.execute(_ddl)
        except sqlite3.OperationalError:
            pass
    _ver = _db.execute("PRAGMA user_version").fetchone()[0]
    if _ver < 1:
        try:
            _db.execute(
                "INSERT INTO operations(ts,user_id,target,method,kind) "
                "SELECT ts,user_id,target,'legacy','legacy' FROM ops"
            )
        except sqlite3.OperationalError:
            pass
    if _ver < 2:
        try:
            _db.execute("INSERT INTO free_log(user_id,method,ts) SELECT user_id,method,ts FROM free_used")
        except sqlite3.OperationalError:
            pass
        _db.execute("UPDATE users SET lang='ar' WHERE lang IS NULL OR lang=''")
    _db.execute("PRAGMA user_version=2")
    _db.commit()


def now_ts() -> int:
    return int(time.time())


def today_start() -> int:
    n = datetime.now(timezone.utc) + timedelta(hours=TZ_OFFSET)
    midnight = n.replace(hour=0, minute=0, second=0, microsecond=0)
    return int((midnight - timedelta(hours=TZ_OFFSET)).timestamp())


def fmt_ts(ts: int, fmt: str = "%d/%m %H:%M") -> str:
    return (datetime.fromtimestamp(ts, timezone.utc) + timedelta(hours=TZ_OFFSET)).strftime(fmt)


def detect_lang(code) -> str:
    return "ar" if (code or "").lower().startswith("ar") else "en"


def upsert_user(u):
    db_exec(
        "INSERT INTO users(id,name,username,joined,lang) VALUES(?,?,?,?,?) "
        "ON CONFLICT(id) DO UPDATE SET name=excluded.name, username=excluded.username, "
        "lang=CASE WHEN users.lang IS NULL OR users.lang='' THEN excluded.lang ELSE users.lang END",
        (u.id, u.first_name or "", u.username or "", now_ts(), detect_lang(getattr(u, "language_code", None))),
    )


def ensure_user(uid: int):
    db_exec("INSERT OR IGNORE INTO users(id,name,username,joined) VALUES(?,?,?,?)",
            (uid, "", "", now_ts()))


def db_user(uid: int):
    return db_exec("SELECT * FROM users WHERE id=?", (uid,), "one")


def get_lang(uid: int) -> str:
    r = db_user(uid)
    lang = r["lang"] if r else ""
    return lang if lang in ("ar", "en") else "ar"


def set_lang(uid: int, lang: str):
    ensure_user(uid)
    db_exec("UPDATE users SET lang=? WHERE id=?", (lang, uid))


def is_banned(uid: int) -> bool:
    r = db_user(uid)
    return bool(r and r["banned"])


def set_ban(uid: int, value: int) -> bool:
    return db_exec("UPDATE users SET banned=? WHERE id=?", (value, uid)).rowcount > 0


def sub_until(uid: int) -> int:
    r = db_user(uid)
    return int(r["sub_until"] or 0) if r else 0


def sub_active(uid: int) -> bool:
    return sub_until(uid) > now_ts()


def add_sub(uid: int, days: int) -> int:
    ensure_user(uid)
    new = max(sub_until(uid), now_ts()) + days * 86400
    db_exec("UPDATE users SET sub_until=? WHERE id=?", (new, uid))
    return new


def clear_sub(uid: int) -> bool:
    ensure_user(uid)
    db_exec("UPDATE users SET sub_until=0 WHERE id=?", (uid,))
    return True


def free_count(uid: int) -> int:
    return db_exec("SELECT COUNT(*) c FROM free_log WHERE user_id=?", (uid,), "one")["c"]


def free_left(uid: int) -> int:
    return max(0, FREE_TRIALS - free_count(uid))


def claim_free(uid: int, method: str) -> int:
    with _lock:
        n = _db.execute("SELECT COUNT(*) FROM free_log WHERE user_id=?", (uid,)).fetchone()[0]
        if n >= FREE_TRIALS:
            return 0
        cur = _db.execute("INSERT INTO free_log(user_id,method,ts) VALUES(?,?,?)", (uid, method, now_ts()))
        _db.commit()
        return cur.lastrowid


def release_free(free_id: int):
    db_exec("DELETE FROM free_log WHERE id=?", (free_id,))


def log_op(uid: int, target: int, method: str, kind: str, ref: str = "") -> int:
    cur = db_exec("INSERT INTO operations(ts,user_id,target,method,kind,ref) VALUES(?,?,?,?,?,?)",
                  (now_ts(), uid, target, method, kind, ref))
    return cur.lastrowid


def drop_op(op_id: int):
    db_exec("DELETE FROM operations WHERE id=?", (op_id,))


def op_get(op_id: int):
    return db_exec("SELECT * FROM operations WHERE id=?", (op_id,), "one")


def op_mark_refunded(op_id: int) -> bool:
    return db_exec("UPDATE operations SET refunded=1 WHERE id=? AND refunded=0", (op_id,)).rowcount == 1


def op_unmark_refunded(op_id: int):
    db_exec("UPDATE operations SET refunded=0 WHERE id=?", (op_id,))


def reports_count(uid: int) -> int:
    return db_exec("SELECT COUNT(*) c FROM operations WHERE user_id=? AND refunded=1", (uid,), "one")["c"]


def ops_count(uid: int) -> int:
    return db_exec("SELECT COUNT(*) c FROM operations WHERE user_id=? AND refunded=0", (uid,), "one")["c"]


def recent_targets(uid: int, limit: int = RECENT_LIMIT):
    return db_exec(
        "SELECT target, MAX(id) m FROM operations "
        "WHERE user_id=? AND refunded=0 AND kind!='legacy' "
        "GROUP BY target ORDER BY m DESC LIMIT ?", (uid, limit), "all")


def pay_exists(charge_id: str) -> bool:
    return db_exec("SELECT 1 FROM payments WHERE charge_id=?", (charge_id,), "one") is not None


def pay_add(charge_id: str, uid: int, target: int, method: str, stars: int):
    db_exec("INSERT OR IGNORE INTO payments VALUES(?,?,?,?,?,?,?)",
            (charge_id, uid, target, method, stars, now_ts(), "paid"))


def pay_set_status(charge_id: str, status: str):
    db_exec("UPDATE payments SET status=? WHERE charge_id=?", (status, charge_id))


def fav_get(owner: int, target: int):
    return db_exec("SELECT * FROM favorites WHERE owner=? AND target=?", (owner, target), "one")


def fav_count(owner: int) -> int:
    return db_exec("SELECT COUNT(*) c FROM favorites WHERE owner=?", (owner,), "one")["c"]


def fav_add(owner: int, target: int, alias: str):
    db_exec("INSERT OR REPLACE INTO favorites VALUES(?,?,?,?)", (owner, target, alias, now_ts()))


def fav_del(owner: int, target: int):
    db_exec("DELETE FROM favorites WHERE owner=? AND target=?", (owner, target))


def fav_list(owner: int):
    return db_exec("SELECT * FROM favorites WHERE owner=? ORDER BY created DESC", (owner,), "all")


def get_stats() -> dict:
    q = lambda s, p=(): db_exec(s, p, "one")[0]
    ts = today_start()
    return {
        "users": q("SELECT COUNT(*) FROM users"),
        "new_today": q("SELECT COUNT(*) FROM users WHERE joined>=?", (ts,)),
        "subs": q("SELECT COUNT(*) FROM users WHERE sub_until>?", (now_ts(),)),
        "banned": q("SELECT COUNT(*) FROM users WHERE banned=1"),
        "ops": q("SELECT COUNT(*) FROM operations WHERE refunded=0"),
        "ops_today": q("SELECT COUNT(*) FROM operations WHERE ts>=? AND refunded=0", (ts,)),
        "ops_free": q("SELECT COUNT(*) FROM operations WHERE kind='free' AND refunded=0"),
        "ops_paid": q("SELECT COUNT(*) FROM operations WHERE kind='paid' AND refunded=0"),
        "ops_sub": q("SELECT COUNT(*) FROM operations WHERE kind IN ('sub','owner')"),
        "stars": q("SELECT COALESCE(SUM(stars),0) FROM payments WHERE status='paid'"),
        "favs": q("SELECT COUNT(*) FROM favorites"),
    }


def B(text, cb=None, url=None, style=None):
    kw = {}
    if cb is not None:
        kw["callback_data"] = cb
    if url is not None:
        kw["url"] = url
    if style and STYLES_OK:
        kw["style"] = getattr(ButtonStyle, style)
    try:
        return InlineKeyboardButton(text, **kw)
    except TypeError:
        kw.pop("style", None)
        return InlineKeyboardButton(text, **kw)


def kb(*rows):
    return InlineKeyboardMarkup([list(r) for r in rows])


def is_owner(uid) -> bool:
    return uid == OWNER_ID


_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")


def parse_id(text: str):
    t = (text or "").strip().translate(_DIGITS)
    if re.fullmatch(r"\d{1,15}", t) and int(t) > 0:
        return int(t)
    return None


def bar(done: int, total: int, size: int = 12) -> str:
    n = int(size * done / total) if total else size
    return "█" * n + "░" * (size - n)


def fmt_uptime() -> str:
    s = int(time.time() - START_TIME)
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, _ = divmod(s, 60)
    return f"{d}ي {h}س {m}د"


def mlabel(method: str, L: str = "ar") -> str:
    return f"{METHODS[method]} {METHOD_NAMES[method][L]}"


STATE: dict[int, dict] = {}
LAST_REQ: dict[int, float] = {}
LAST_ACTION: dict[int, float] = {}
SUBREQ: dict[int, float] = {}
RECENT: dict[tuple, float] = {}
BC = {"running": False, "cancel": False}
_DEV_URL = None
_CMDS_SET = False


async def dev_url(client: Client) -> str:
    global _DEV_URL
    if _DEV_URL:
        return _DEV_URL
    try:
        u = await client.get_users(OWNER_ID)
        if u.username:
            _DEV_URL = f"https://t.me/{u.username}"
    except Exception:
        pass
    return _DEV_URL or f"tg://user?id={OWNER_ID}"


async def notify_dev(client: Client, text: str, markup=None):
    try:
        await client.send_message(OWNER_ID, text, reply_markup=markup)
    except Exception as e:
        log.warning("notify_dev failed: %s", e)


async def setup_commands(client: Client):
    global _CMDS_SET
    if _CMDS_SET:
        return
    _CMDS_SET = True
    names = ("start", "help", "favs", "plan", "lang", "paysupport")
    try:
        for code, lang in (("", "en"), ("ar", "ar"), ("en", "en")):
            cmds = [BotCommand(c, tr(lang, f"cmd_{c}")) for c in names]
            await client.set_bot_commands(cmds, language_code=code)
    except Exception as e:
        log.warning("set_bot_commands failed: %s", e)


_TG_PARAM = re.compile(r"(?:^|[?&])(?:id|user_id)=(\d{1,15})(?!\d)")
_USERNAME = re.compile(
    r"(?:@|(?:https?://)?(?:www\.)?t(?:elegram)?\.me/)([A-Za-z][A-Za-z0-9_]{3,31})(?![A-Za-z0-9_])", re.I)
_RESERVED = {"joinchat", "addstickers", "addemoji", "share", "proxy", "socks", "setlanguage", "iv", "login", "boost"}
_NUMS = re.compile(r"(?<![\d-])\d{5,15}(?!\d)")
_CHAT_ID = re.compile(r"(?<!\d)-100\d{6,}")


def classify_text(text: str):
    t = (text or "").strip().translate(_DIGITS)
    if not t:
        return "none", None
    exact = parse_id(t)
    if exact is not None:
        return "id", exact
    m = _TG_PARAM.search(t)
    if m and "tg://" in t.lower():
        return "id", int(m.group(1))
    if _CHAT_ID.search(t):
        return "chat_id", None
    m = _USERNAME.search(t)
    if m and m.group(1).lower() not in _RESERVED:
        return "username", m.group(1)
    nums = set(_NUMS.findall(t))
    if len(nums) == 1:
        return "id", int(nums.pop())
    if len(nums) > 1:
        return "many", None
    return "none", None


async def username_to_id(client: Client, uname: str) -> Optional[int]:
    try:
        u = await client.get_users(uname)
        if isinstance(u, list):
            u = u[0]
        return u.id
    except Exception:
        pass
    try:
        c = await client.get_chat(uname)
        return c.id if c.id > 0 else None
    except Exception:
        return None


async def extract_target(client: Client, m: Message, L: str):
    fu = getattr(m, "forward_from", None)
    fo = getattr(m, "forward_origin", None)
    if fu is None and fo is not None:
        fu = getattr(fo, "sender_user", None)
    if fu is not None and getattr(fu, "id", None):
        return fu.id, ("fwd", None), None
    if (getattr(m, "forward_sender_name", None) or getattr(m, "forward_from_chat", None) or fo is not None):
        return None, None, tr(L, "err_fwd")

    c = getattr(m, "contact", None)
    if c is not None:
        if getattr(c, "user_id", None):
            return c.user_id, ("contact", None), None
        return None, None, tr(L, "err_contact")

    text = (m.text or m.caption or "").strip()
    if not text:
        return None, None, tr(L, "err_not_text")
    kind, val = classify_text(text)
    if kind == "id":
        return val, None, None
    if kind == "username":
        tid = await username_to_id(client, val)
        if tid:
            return tid, ("user", f"@{val}"), None
        return None, None, tr(L, "err_username", u=html.escape(val))
    if kind == "chat_id":
        return None, None, tr(L, "err_chat_id")
    if kind == "many":
        return None, None, tr(L, "err_many")
    return None, None, None


def access_mode(uid: int, method: str = "") -> str:
    if is_owner(uid):
        return "owner"
    if sub_active(uid):
        return "sub"
    if free_left(uid) > 0:
        return "free"
    return "pay"


def mode_tag(mode: str) -> str:
    return {"owner": "✅", "sub": "✅", "free": "", "pay": "⭐"}[mode]


def status_line(uid: int, L: str) -> str:
    if is_owner(uid):
        return tr(L, "st_owner")
    if sub_active(uid):
        return tr(L, "st_sub")
    left = free_left(uid)
    if left > 0:
        return tr(L, "st_free", free=free_phrase(L, left))
    return tr(L, "st_nofree", price=STAR_PRICE)


def home_markup(uid: int, L: str):
    other = "en" if L == "ar" else "ar"
    rows = [
        [B(tr(L, "btn_myid"), "myid", style="SUCCESS"), B(tr(L, "btn_recent"), "recent", style="PRIMARY")],
        [B(tr(L, "btn_favs"), "favs:0", style="PRIMARY"), B(tr(L, "btn_plan"), "plan", style="SUCCESS")],
        [B(tr(L, "btn_help"), "help", style="PRIMARY"), B(tr(L, "btn_lang"), f"setlang:{other}", style="PRIMARY")],
    ]
    if is_owner(uid):
        rows.append([B(tr(L, "btn_admin"), "adm:home", style="DANGER")])
    return kb(*rows)


def home_btn(L: str, style="PRIMARY"):
    return B(tr(L, "btn_home"), "home", style=style)


def welcome_text(uid: int, name: str, L: str) -> str:
    return tr(L, "welcome", name=html.escape(name), status=status_line(uid, L))


def help_text(L: str) -> str:
    return tr(L, "help", free=free_phrase(L, FREE_TRIALS), price=STAR_PRICE)


def build_card(viewer: int, target: int, L: str, back: str = None, via=None, prefix: str = ""):
    extra = ""
    if via:
        kind, val = via
        extra += tr(L, f"via_{kind}", u=html.escape(val or ""))
    fav = fav_get(viewer, target)
    if fav:
        extra += tr(L, "card_alias", alias=html.escape(fav["alias"]))
    mode = access_mode(viewer)
    if mode == "owner":
        legend = tr(L, "legend_owner")
    elif mode == "sub":
        legend = tr(L, "legend_sub")
    elif mode == "free":
        legend = tr(L, "legend_free", free=free_phrase(L, free_left(viewer)))
    else:
        legend = tr(L, "legend_pay", price=STAR_PRICE)
    text = prefix + tr(L, "card", target=target, extra=extra, legend=legend)
    return text, card_markup(viewer, target, L, back)


def card_markup(viewer: int, target: int, L: str, back: str = None):
    tag = mode_tag(access_mode(viewer))

    def mb(method):
        return B(f"{mlabel(method, L)} {tag}".strip(), f"m:{method}:{target}", style=METHOD_STYLE[method])

    fav = fav_get(viewer, target)
    fav_btn = (B(tr(L, "btn_unsave"), f"favdel:{target}", style="DANGER") if fav
               else B(tr(L, "btn_save"), f"save:{target}", style="SUCCESS"))
    rows = [
        [mb("chat"), mb("profile")],
        [mb("username"), mb("web")],
        [mb("info"), mb("photo")],
        [fav_btn, B(tr(L, "btn_favs_open"), "favs:0", style="PRIMARY")],
    ]
    if back:
        rows.append([B(tr(L, "btn_back"), back, style="PRIMARY")])
    return kb(*rows)


def favs_view(owner: int, page: int, L: str):
    items = fav_list(owner)
    total = len(items)
    pages = max(1, -(-total // FAVS_PER_PAGE))
    page = max(0, min(page, pages - 1))
    chunk = items[page * FAVS_PER_PAGE:(page + 1) * FAVS_PER_PAGE]

    if not items:
        return tr(L, "fav_empty"), kb([home_btn(L)])

    text = tr(L, "fav_list", n=total, max=MAX_FAVS, page=page + 1, pages=pages)
    rows = [
        [B(f"👤 {f['alias']}", f"fav:{f['target']}:{page}", style="PRIMARY"),
         B("🗑", f"favdel:{f['target']}", style="DANGER")]
        for f in chunk
    ]
    nav = []
    if page > 0:
        nav.append(B(tr(L, "btn_prev"), f"favs:{page - 1}", style="PRIMARY"))
    if page < pages - 1:
        nav.append(B(tr(L, "btn_next"), f"favs:{page + 1}", style="PRIMARY"))
    if nav:
        rows.append(nav)
    rows.append([home_btn(L, "SUCCESS")])
    return text, kb(*rows)


def recent_view(uid: int, L: str):
    rows = recent_targets(uid)
    if not rows:
        return tr(L, "recent_empty"), kb([home_btn(L)])
    buttons = []
    for r in rows:
        t = r["target"]
        fav = fav_get(uid, t)
        label = f"⭐ {fav['alias']}" if fav else f"🆔 {t}"
        buttons.append([B(label, f"rc:{t}", style="PRIMARY")])
    buttons.append([home_btn(L, "SUCCESS")])
    return tr(L, "recent_list"), kb(*buttons)


def free_status(uid: int, L: str) -> str:
    left = free_left(uid)
    if FREE_TRIALS == 1:
        return tr(L, "free_avail" if left else "free_used")
    return tr(L, "free_left_n", left=left, n=FREE_TRIALS)


def plan_view(uid: int, L: str):
    until = sub_until(uid)
    if is_owner(uid):
        status = tr(L, "plan_owner")
    elif until > now_ts():
        days = max(1, -(-(until - now_ts()) // 86400))
        status = tr(L, "plan_sub", date=fmt_ts(until, "%d/%m/%Y"), days=days)
    else:
        status = tr(L, "plan_none")
    text = tr(L, "plan", status=status, free=free_status(uid, L), ops=ops_count(uid), price=STAR_PRICE)
    rows = []
    if not is_owner(uid) and until <= now_ts():
        rows.append([B(tr(L, "btn_subreq_long"), "subreq", style="PRIMARY")])
    rows.append([home_btn(L, "SUCCESS")])
    return text, kb(*rows)


class Unavailable(Exception):

    def __init__(self, key: str):
        super().__init__(key)
        self.key = key


@dataclass
class Result:
    text: str
    markup: Optional[InlineKeyboardMarkup] = None
    photo: object = None


async def resolve(client: Client, target: int):
    user = chat = None
    try:
        user = await client.get_users(target)
    except Exception:
        pass
    try:
        chat = await client.get_chat(target)
    except Exception:
        pass
    return user, chat


def _first(*vals):
    for v in vals:
        if v:
            return v
    return None


async def prepare(client: Client, method: str, target: int, L: str) -> Result:
    head = f"{METHODS[method]} <b>{METHOD_NAMES[method][L]}</b>\n{LINE}\n🆔 <code>{target}</code>"

    if method == "chat":
        return Result(head + tr(L, "hint_link"),
                      kb([B(tr(L, "open_chat"), url=f"tg://openmessage?user_id={target}", style="PRIMARY")]))

    if method == "profile":
        return Result(head + tr(L, "hint_link"),
                      kb([B(tr(L, "open_profile"), url=f"tg://user?id={target}", style="SUCCESS")]))

    if method == "web":
        return Result(head + tr(L, "hint_link"),
                      kb([B(tr(L, "open_web"), url=f"https://web.telegram.org/k/#{target}", style="PRIMARY")]))

    user, chat = await resolve(client, target)
    row = db_user(target)

    if method == "username":
        uname = _first(getattr(user, "username", None), getattr(chat, "username", None),
                       row["username"] if row else None)
        if not uname:
            raise Unavailable("un_username")
        return Result(f"{head}\n🏷 @{html.escape(uname)}",
                      kb([B(tr(L, "open_username"), url=f"https://t.me/{uname}", style="PRIMARY")]))

    if method == "info":
        if not (user or chat or (row and (row["name"] or row["username"]))):
            raise Unavailable("un_info")
        first = _first(getattr(user, "first_name", None), getattr(chat, "first_name", None),
                       row["name"] if row else None) or ""
        last = _first(getattr(user, "last_name", None), getattr(chat, "last_name", None)) or ""
        full = html.escape(f"{first} {last}".strip())
        uname = _first(getattr(user, "username", None), getattr(chat, "username", None),
                       row["username"] if row else None)
        bio = getattr(chat, "bio", None)
        lines = [head]
        if full:
            lines.append(tr(L, "i_name", v=f'<a href="tg://user?id={target}">{full}</a>'))
        if uname:
            lines.append(tr(L, "i_user", v=html.escape(uname)))
        if bio:
            lines.append(tr(L, "i_bio", v=html.escape(bio[:200])))
        src = user or chat
        if getattr(src, "is_premium", False):
            lines.append(tr(L, "i_premium"))
        if getattr(src, "is_bot", False):
            lines.append(tr(L, "i_bot"))
        if getattr(src, "is_verified", False):
            lines.append(tr(L, "i_verified"))
        if getattr(src, "is_scam", False):
            lines.append(tr(L, "i_scam"))
        if getattr(src, "is_fake", False):
            lines.append(tr(L, "i_fake"))
        if getattr(user, "language_code", None):
            lines.append(tr(L, "i_lang", v=html.escape(user.language_code)))
        if getattr(user, "dc_id", None):
            lines.append(tr(L, "i_dc", v=user.dc_id))
        return Result("\n".join(lines))

    if method == "photo":
        photo = getattr(chat, "photo", None)
        if not photo:
            raise Unavailable("un_photo_none")
        buf = await client.download_media(photo.big_file_id, in_memory=True)
        if buf is None:
            raise Unavailable("un_photo_fail")
        buf.name = "photo.jpg"
        return Result(head, None, buf)

    raise Unavailable("un_unknown")


async def deliver(client: Client, chat_id: int, uid: int, target: int, method: str, kind: str,
                  res: Result, L: str, ref: str = "") -> int:
    op_id = log_op(uid, target, method, kind, ref)
    text, markup = res.text, res.markup
    if method in LINK_METHODS and kind in ("free", "paid"):
        rows = list(markup.inline_keyboard) if markup else []
        rows.append([B(tr(L, "btn_bad"), f"bad:{op_id}", style="DANGER")])
        markup = InlineKeyboardMarkup(rows)
        text += tr(L, "hint_report")
    try:
        if res.photo is not None:
            await client.send_photo(chat_id, res.photo, caption=text, reply_markup=markup)
        else:
            await client.send_message(chat_id, text, reply_markup=markup)
    except Exception:
        drop_op(op_id)
        raise
    return op_id


def paywall(method: str, target: int, L: str):
    text = tr(L, "paywall", method=mlabel(method, L), price=STAR_PRICE)
    markup = kb(
        [B(tr(L, "btn_pay", price=STAR_PRICE), f"pay:{method}:{target}", style="SUCCESS"),
         B(tr(L, "btn_subreq"), "subreq", style="PRIMARY")],
    )
    return text, markup


async def send_invoice_for(client: Client, q: CallbackQuery, method: str, target: int, L: str):
    n = METHOD_NAMES[method][L]
    try:
        await client.send_invoice(
            chat_id=q.from_user.id,
            title=n[:32],
            description=tr(L, "invoice_desc", emoji=METHODS[method], name=n, target=target)[:255],
            payload=f"m:{method}:{target}",
            currency="XTR",
            prices=[LabeledPrice(label=n[:32], amount=STAR_PRICE)],
            provider_token="",
        )
        await q.answer()
    except Exception as ex:
        log.error("send_invoice failed: %s", ex)
        await q.answer(tr(L, "t_invoice_fail"), show_alert=True)


async def process_method(client: Client, q: CallbackQuery, method: str, target: int, pay_intent=False):
    uid = q.from_user.id
    L = get_lang(uid)
    now = time.time()
    if now - LAST_ACTION.get(uid, 0) < 1.0:
        return await q.answer(tr(L, "t_wait"))
    LAST_ACTION[uid] = now

    try:
        res = await prepare(client, method, target, L)
    except Unavailable as ex:
        return await q.answer(tr(L, ex.key), show_alert=True)
    except Exception as ex:
        log.warning("prepare failed (%s): %s", method, ex)
        return await q.answer(tr(L, "t_err"), show_alert=True)

    mode = access_mode(uid, method)
    free_id = 0
    if mode == "free":
        free_id = claim_free(uid, method)
        if not free_id:
            mode = "pay"

    if mode == "pay":
        if pay_intent:
            return await send_invoice_for(client, q, method, target, L)
        await q.answer()
        text, markup = paywall(method, target, L)
        return await q.message.reply(text, reply_markup=markup)

    try:
        await deliver(client, q.message.chat.id, uid, target, method, mode, res, L,
                      ref=str(free_id) if free_id else "")
    except Exception as ex:
        log.error("deliver failed: %s", ex)
        if free_id:
            release_free(free_id)
        return await q.answer(tr(L, "t_send_fail"), show_alert=True)

    await q.answer(tr(L, "t_free_used") if mode == "free" else tr(L, "t_done"))

    try:
        if q.message.reply_markup:
            back = next((b.callback_data for r in q.message.reply_markup.inline_keyboard
                         for b in r if b.text.startswith("🔙")), None)
            await q.message.edit_reply_markup(card_markup(uid, target, L, back))
    except Exception:
        pass


async def handle_report(client: Client, q: CallbackQuery, op_id: int):
    uid = q.from_user.id
    L = get_lang(uid)
    op = op_get(op_id)
    if not op or op["user_id"] != uid:
        return await q.answer(tr(L, "t_invalid"), show_alert=True)
    if op["refunded"]:
        return await q.answer(tr(L, "bad_done"), show_alert=True)
    if op["kind"] not in ("free", "paid"):
        return await q.answer(tr(L, "bad_nothing"), show_alert=True)
    if reports_count(uid) >= MAX_REPORTS:
        return await q.answer(tr(L, "bad_limit"), show_alert=True)
    if not op_mark_refunded(op_id):
        return await q.answer(tr(L, "bad_done"), show_alert=True)

    if op["kind"] == "free":
        try:
            release_free(int(op["ref"]))
        except (TypeError, ValueError):
            pass
        msg = tr(L, "bad_free_back")
    else:
        ok = False
        try:
            ok = await client.refund_star_payment(uid, op["ref"])
        except Exception as ex:
            log.error("report refund failed: %s", ex)
        if not ok:
            op_unmark_refunded(op_id)
            await notify_dev(client, f"⚠️ <b>فشل استرداد بلاغ</b>\n👤 <code>{uid}</code>\n"
                                     f"<code>/refund {uid} {op['ref']}</code>")
            return await q.answer(tr(L, "bad_refund_failed"), show_alert=True)
        pay_set_status(op["ref"], "refunded")
        msg = tr(L, "bad_star_back")

    try:
        rows = [list(r) for r in q.message.reply_markup.inline_keyboard]
        rows = [r for r in rows if not any((b.callback_data or "").startswith("bad:") for b in r)]
        await q.message.edit_reply_markup(InlineKeyboardMarkup(rows) if rows else None)
    except Exception:
        pass
    await q.answer(msg, show_alert=True)
    await notify_dev(
        client,
        f"📝 <b>بلاغ «الرابط ما اشتغل»</b>\n👤 <code>{uid}</code>\n"
        f"{mlabel(op['method'])} → <code>{op['target']}</code>\n"
        f"النوع: {KIND_ICON.get(op['kind'], '')} {op['kind']} (تم الإرجاع)")


async def answer_checkout(q, err: Optional[str]):
    ok = err is None
    try:
        if ok:
            await q.answer(ok=True)
        else:
            await q.answer(ok=False, error_message=err)
    except TypeError:
        if ok:
            await q.answer(success=True)
        else:
            await q.answer(error=err)


@app.on_pre_checkout_query()
async def pre_checkout(client, q):
    L = get_lang(q.from_user.id)
    err = None
    try:
        kind, method, target = q.invoice_payload.split(":")
        if kind != "m" or method not in METHODS or not target.isdigit():
            err = tr(L, "co_invalid")
        elif q.currency != "XTR" or q.total_amount != STAR_PRICE:
            err = tr(L, "co_amount")
        elif is_banned(q.from_user.id):
            err = tr(L, "co_banned")
    except Exception:
        err = tr(L, "co_invalid")
    await answer_checkout(q, err)


async def auto_refund(client: Client, uid: int, charge_id: str, reason: str):
    L = get_lang(uid)
    try:
        ok = await client.refund_star_payment(uid, charge_id)
        if ok:
            pay_set_status(charge_id, "refunded")
            await client.send_message(uid, tr(L, "refund_auto"))
            return
        raise RuntimeError("refund returned False")
    except Exception as ex:
        log.error("auto refund failed: %s", ex)
        pay_set_status(charge_id, "refund_failed")
        await notify_dev(
            client,
            f"⚠️ <b>فشل الاسترداد التلقائي</b>\n👤 <code>{uid}</code>\nالسبب: {html.escape(reason)}\n"
            f"استخدم: <code>/refund {uid} {charge_id}</code>",
        )


@app.on_message(filters.private & filters.successful_payment, group=-2)
async def on_paid(client, m: Message):
    sp = m.successful_payment
    uid = m.from_user.id
    L = get_lang(uid)
    charge = sp.telegram_payment_charge_id
    try:
        if pay_exists(charge):
            raise StopPropagation
        _, method, target = sp.invoice_payload.split(":")
        target = int(target)
        if sp.currency != "XTR" or method not in METHODS:
            raise ValueError("unexpected payment")
    except StopPropagation:
        raise
    except Exception as ex:
        log.error("bad payment payload: %s | %s", sp.invoice_payload, ex)
        await notify_dev(client, f"⚠️ دفعة غير مفهومة من <code>{uid}</code>\ncharge: <code>{charge}</code>")
        raise StopPropagation

    pay_add(charge, uid, target, method, sp.total_amount)
    try:
        res = await prepare(client, method, target, L)
        await deliver(client, m.chat.id, uid, target, method, "paid", res, L, ref=charge)
    except Unavailable as ex:
        await auto_refund(client, uid, charge, ex.key)
    except Exception as ex:
        log.error("delivery after payment failed: %s", ex)
        await auto_refund(client, uid, charge, f"delivery error: {ex}")
    raise StopPropagation


def admin_markup():
    return kb(
        [B("📊 الإحصائيات", "adm:stats", style="PRIMARY"), B("📢 إذاعة", "adm:bc", style="SUCCESS")],
        [B("💎 تفعيل اشتراك", "adm:sub", style="SUCCESS"), B("🔕 إلغاء اشتراك", "adm:unsub", style="DANGER")],
        [B("💎 المشتركون", "adm:subs", style="PRIMARY"), B("📜 آخر العمليات", "adm:log", style="PRIMARY")],
        [B("🔎 سجل مستخدم", "adm:ulog", style="SUCCESS"), B("🌟 المدفوعات", "adm:pay", style="SUCCESS")],
        [B("🚫 حظر", "adm:ban", style="DANGER"), B("✅ فك حظر", "adm:unban", style="SUCCESS")],
        [B("📋 المحظورون", "adm:banned", style="PRIMARY"), B("🏠 خروج", "home", style="DANGER")],
    )


ADMIN_TEXT = (
    f"👑 <b>لوحة تحكم المطور</b>\n{LINE}\n"
    "مرحباً بك يا مطور 🌹\nاختر من الأزرار أدناه:"
)
DENY_TEXT = "⛔ هذه اللوحة مخصصة للمطور فقط."
BACK_ADMIN = kb([B("🔙 رجوع", "adm:home", style="PRIMARY")])


def stats_text() -> str:
    s = get_stats()
    return (
        f"📊 <b>إحصائيات البوت</b>\n{LINE}\n"
        f"👥 المستخدمين: <b>{s['users']}</b>  (🆕 اليوم: {s['new_today']})\n"
        f"💎 المشتركون: <b>{s['subs']}</b>\n"
        f"🚫 المحظورون: <b>{s['banned']}</b>\n{LINE}\n"
        f"⚙️ العمليات: <b>{s['ops']}</b>  (📅 اليوم: {s['ops_today']})\n"
        f"├ 🎁 مجانية: {s['ops_free']}\n"
        f"├ ⭐ مدفوعة: {s['ops_paid']}\n"
        f"└ 💎 اشتراك/مطور: {s['ops_sub']}\n"
        f"🌟 النجوم المحصّلة: <b>{s['stars']}</b>\n"
        f"⭐ المحفوظات: <b>{s['favs']}</b>\n"
        f"⏱ مدة التشغيل: <b>{fmt_uptime()}</b>\n{LINE}"
    )


def _uname(r) -> str:
    return html.escape((r["name"] or "").strip() or "—")


def recent_ops_text() -> str:
    rows = db_exec(
        "SELECT o.*, u.name FROM operations o LEFT JOIN users u ON u.id=o.user_id "
        "WHERE o.kind IN ('free','paid') ORDER BY o.id DESC LIMIT 20", (), "all")
    if not rows:
        return f"📜 <b>عمليات غير المشتركين</b>\n{LINE}\nلا توجد عمليات بعد."
    body = "\n".join(
        f"{KIND_ICON.get(r['kind'], '•')} {fmt_ts(r['ts'])} • <code>{r['user_id']}</code> {_uname(r)}\n"
        f"   ↳ {mlabel(r['method']) if r['method'] in METHODS else r['method']} → <code>{r['target']}</code>"
        for r in rows)
    return f"📜 <b>آخر عمليات غير المشتركين</b>\n{LINE}\n{body}"


def user_log_text(target: int):
    u = db_user(target)
    if not u:
        return None
    rows = db_exec("SELECT * FROM operations WHERE user_id=? ORDER BY id DESC LIMIT 25", (target,), "all")
    sub = (f"✅ حتى {fmt_ts(u['sub_until'], '%d/%m/%Y')}" if u["sub_until"] > now_ts() else "❌ غير مشترك")
    paid = db_exec("SELECT COUNT(*) c, COALESCE(SUM(stars),0) s FROM payments WHERE user_id=? AND status='paid'",
                   (target,), "one")
    head = (
        f"🔎 <b>سجل المستخدم</b>\n{LINE}\n"
        f"🆔 <code>{target}</code> • {_uname(u)}\n"
        f"💎 الاشتراك: {sub}\n"
        f"⭐ مدفوعاته: {paid['c']} عملية ({paid['s']} نجمة)\n"
        f"⚙️ إجمالي عملياته: {ops_count(target)}\n{LINE}\n"
    )
    if not rows:
        return head + "لا توجد عمليات."
    body = "\n".join(
        f"{KIND_ICON.get(r['kind'], '•')} {fmt_ts(r['ts'])} • "
        f"{mlabel(r['method']) if r['method'] in METHODS else r['method']} → <code>{r['target']}</code>"
        for r in rows)
    return head + body


def payments_text() -> str:
    rows = db_exec("SELECT * FROM payments ORDER BY ts DESC LIMIT 10", (), "all")
    if not rows:
        return f"🌟 <b>المدفوعات</b>\n{LINE}\nلا توجد مدفوعات بعد."
    icon = {"paid": "✅", "refunded": "↩️", "refund_failed": "⚠️"}
    body = "\n\n".join(
        f"{icon.get(r['status'], '•')} {fmt_ts(r['ts'])} • <code>{r['user_id']}</code> • {r['stars']}⭐ • "
        f"{mlabel(r['method']) if r['method'] in METHODS else r['method']}\n<code>{r['charge_id']}</code>"
        for r in rows)
    return (f"🌟 <b>آخر المدفوعات</b>\n{LINE}\n{body}\n{LINE}\n"
            "للاسترداد: <code>/refund USER_ID CHARGE_ID</code>")


async def run_broadcast(client: Client, chat_id: int, status_id: int, src_chat: int, src_msg: int):
    ids = [r["id"] for r in db_exec("SELECT id FROM users WHERE banned=0", (), "all")]
    total, sent, failed = len(ids), 0, 0
    BC.update(running=True, cancel=False)
    cancel_kb = kb([B("⛔ إلغاء الإذاعة", "bc:cancel", style="DANGER")])

    async def render(done: int, final: str = None):
        head = final or "📢 <b>جاري الإذاعة...</b>"
        txt = (
            f"{head}\n{LINE}\n<code>{bar(done, total)}</code> {int(100 * done / max(total, 1))}%\n"
            f"✅ نجحت: <b>{sent}</b>\n❌ فشلت: <b>{failed}</b>\n👥 الإجمالي: <b>{total}</b>"
        )
        try:
            await client.edit_message_text(
                chat_id, status_id, txt, reply_markup=None if final else cancel_kb
            )
        except Exception:
            pass

    done = 0
    try:
        for uid in ids:
            if BC["cancel"]:
                break
            try:
                await client.copy_message(uid, src_chat, src_msg)
                sent += 1
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                try:
                    await client.copy_message(uid, src_chat, src_msg)
                    sent += 1
                except Exception:
                    failed += 1
            except (UserIsBlocked, InputUserDeactivated, PeerIdInvalid):
                failed += 1
            except Exception as e:
                log.warning("broadcast error %s: %s", uid, e)
                failed += 1
            done += 1
            if done % 15 == 0:
                await render(done)
            await asyncio.sleep(0.05)
    finally:
        cancelled = BC["cancel"]
        BC.update(running=False, cancel=False)
        await render(done, "⛔ <b>تم إلغاء الإذاعة</b>" if cancelled else "🎉 <b>اكتملت الإذاعة بنجاح</b>")


async def activate_sub(client: Client, target: int, days: int) -> str:
    until = add_sub(target, days)
    note = ""
    try:
        await client.send_message(
            target, tr(get_lang(target), "sub_activated", date=fmt_ts(until, "%d/%m/%Y")))
    except Exception:
        note = "\n⚠️ تعذر إشعار المستخدم (لم يبدأ البوت أو حظره)."
    return f"✅ تم تفعيل الاشتراك للمستخدم <code>{target}</code> حتى <b>{fmt_ts(until, '%d/%m/%Y')}</b>{note}"


def _boot_commands(client):
    if not _CMDS_SET:
        asyncio.create_task(setup_commands(client))


@app.on_message(filters.private, group=-1)
async def gate_message(client, m: Message):
    if not m.from_user:
        return
    upsert_user(m.from_user)
    _boot_commands(client)
    if not is_owner(m.from_user.id) and is_banned(m.from_user.id):
        await m.reply(tr(get_lang(m.from_user.id), "banned"))
        raise StopPropagation


@app.on_callback_query(group=-1)
async def gate_callback(client, q: CallbackQuery):
    upsert_user(q.from_user)
    _boot_commands(client)
    if not is_owner(q.from_user.id) and is_banned(q.from_user.id):
        await q.answer(tr(get_lang(q.from_user.id), "banned_cb"), show_alert=True)
        raise StopPropagation


async def send_card(m_or_q_message, uid: int, target: int, L: str, via=None, prefix: str = "", back=None):
    text, markup = build_card(uid, target, L, back=back, via=via, prefix=prefix)
    return await m_or_q_message.reply(text, reply_markup=markup)


@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, m: Message):
    uid = m.from_user.id
    L = get_lang(uid)
    STATE.pop(uid, None)
    if len(m.command) > 1:
        kind, val = classify_text(" ".join(m.command[1:]))
        if kind == "id":
            await send_card(m, uid, val, L)
    await m.reply(welcome_text(uid, m.from_user.first_name or ("صديقي" if L == "ar" else "friend"), L),
                  reply_markup=home_markup(uid, L))


@app.on_message(filters.private & filters.command("help"))
async def help_cmd(client, m: Message):
    L = get_lang(m.from_user.id)
    await m.reply(help_text(L), reply_markup=kb([home_btn(L)]))


@app.on_message(filters.private & filters.command("favs"))
async def favs_cmd(client, m: Message):
    text, markup = favs_view(m.from_user.id, 0, get_lang(m.from_user.id))
    await m.reply(text, reply_markup=markup)


@app.on_message(filters.private & filters.command("plan"))
async def plan_cmd(client, m: Message):
    text, markup = plan_view(m.from_user.id, get_lang(m.from_user.id))
    await m.reply(text, reply_markup=markup)


@app.on_message(filters.private & filters.command("lang"))
async def lang_cmd(client, m: Message):
    await m.reply(tr("ar", "lang_pick"),
                  reply_markup=kb([B("🇮🇶 العربية", "setlang:ar", style="SUCCESS"),
                                   B("🇬🇧 English", "setlang:en", style="PRIMARY")]))


@app.on_message(filters.private & filters.command("paysupport"))
async def paysupport_cmd(client, m: Message):
    uid = m.from_user.id
    L = get_lang(uid)
    rows = db_exec("SELECT * FROM payments WHERE user_id=? ORDER BY ts DESC LIMIT 5", (uid,), "all")
    mine = "\n".join(f"• {fmt_ts(r['ts'])} • {r['stars']}⭐ • <code>{r['charge_id']}</code>" for r in rows)
    text = tr(L, "paysupport")
    if mine:
        text += f"\n{LINE}\n{tr(L, 'paysupport_mine')}\n{mine}"
    await m.reply(text, reply_markup=kb([B(tr(L, "btn_dev"), url=await dev_url(client), style="PRIMARY")]))


@app.on_message(filters.private & filters.command("refund"))
async def refund_cmd(client, m: Message):
    if not is_owner(m.from_user.id):
        return await m.reply(DENY_TEXT)
    if len(m.command) != 3 or not m.command[1].isdigit():
        return await m.reply("الاستخدام: <code>/refund USER_ID CHARGE_ID</code>")
    uid, charge = int(m.command[1]), m.command[2]
    try:
        ok = await client.refund_star_payment(uid, charge)
    except Exception as ex:
        return await m.reply(f"❌ فشل الاسترداد: <code>{html.escape(str(ex))}</code>")
    if ok:
        pay_set_status(charge, "refunded")
        try:
            await client.send_message(uid, tr(get_lang(uid), "refund_dev"))
        except Exception:
            pass
        await m.reply("✅ تم الاسترداد.")
    else:
        await m.reply("❌ لم يتم الاسترداد.")


@app.on_message(filters.private & filters.command("cancel"))
async def cancel_cmd(client, m: Message):
    L = get_lang(m.from_user.id)
    if STATE.pop(m.from_user.id, None):
        await m.reply(tr(L, "cancel_ok"))
    else:
        await m.reply(tr(L, "cancel_none"))


@app.on_message(filters.private & filters.command("admin"))
async def admin_cmd(client, m: Message):
    if not is_owner(m.from_user.id):
        return await m.reply(DENY_TEXT)
    await m.reply(ADMIN_TEXT, reply_markup=admin_markup())


@app.on_message(filters.private & ~filters.command(COMMANDS) & ~filters.successful_payment)
async def on_message(client, m: Message):
    uid = m.from_user.id
    L = get_lang(uid)
    st = STATE.get(uid)

    if st:
        mode = st["mode"]

        if mode == "alias":
            alias = (m.text or "").strip()
            if not alias or len(alias) > 24:
                return await m.reply(tr(L, "alias_bad"))
            STATE.pop(uid, None)
            fav_add(uid, st["target"], alias)
            return await send_card(m, uid, st["target"], L,
                                   prefix=tr(L, "alias_saved", alias=html.escape(alias)) + "\n\n")

        if mode in ("ban", "unban") and is_owner(uid):
            target = parse_id(m.text)
            if target is None:
                return await m.reply("⚠️ أرسل أيدي صحيح (أرقام فقط) أو /cancel.")
            STATE.pop(uid, None)
            if is_owner(target):
                return await m.reply("😅 لا يمكنك حظر نفسك!")
            ok = set_ban(target, 1 if mode == "ban" else 0)
            if not ok:
                return await m.reply("❌ هذا المستخدم غير موجود في قاعدة البيانات.")
            msg = "🚫 تم حظر المستخدم" if mode == "ban" else "✅ تم فك الحظر عن المستخدم"
            return await m.reply(f"{msg} <code>{target}</code>", reply_markup=admin_markup())

        if mode == "sub" and is_owner(uid):
            parts = (m.text or "").split()
            target = parse_id(parts[0]) if parts else None
            if target is None:
                return await m.reply("⚠️ أرسل: <code>الأيدي</code> أو <code>الأيدي عدد_الأيام</code>\n(أو /cancel)")
            days = SUB_DAYS
            if len(parts) > 1:
                d = parse_id(parts[1])
                if d is None or d > 3650:
                    return await m.reply("⚠️ عدد الأيام يجب أن يكون رقماً من 1 إلى 3650.")
                days = d
            STATE.pop(uid, None)
            return await m.reply(await activate_sub(client, target, days), reply_markup=admin_markup())

        if mode == "unsub" and is_owner(uid):
            target = parse_id(m.text)
            if target is None:
                return await m.reply("⚠️ أرسل أيدي صحيح (أرقام فقط) أو /cancel.")
            STATE.pop(uid, None)
            clear_sub(target)
            return await m.reply(f"🔕 تم إلغاء اشتراك <code>{target}</code>", reply_markup=admin_markup())

        if mode == "ulog" and is_owner(uid):
            target = parse_id(m.text)
            if target is None:
                return await m.reply("⚠️ أرسل أيدي صحيح (أرقام فقط) أو /cancel.")
            STATE.pop(uid, None)
            text = user_log_text(target)
            return await m.reply(text or "❌ هذا المستخدم غير موجود في قاعدة البيانات.",
                                 reply_markup=BACK_ADMIN)

        if mode == "bc" and is_owner(uid):
            STATE.pop(uid, None)
            STATE[uid] = {"mode": "bc_confirm", "chat": m.chat.id, "msg": m.id}
            count = db_exec("SELECT COUNT(*) c FROM users WHERE banned=0", (), "one")["c"]
            await m.reply("👆 <b>هذه معاينة الرسالة.</b>")
            return await m.reply(
                f"📢 <b>تأكيد الإذاعة</b>\n{LINE}\nسيتم الإرسال إلى <b>{count}</b> مستخدم.\nهل تريد المتابعة؟",
                reply_markup=kb([B("🚀 ابدأ الإذاعة", "bc:go", style="SUCCESS"),
                                 B("❌ إلغاء", "bc:abort", style="DANGER")]),
            )

    now = time.time()
    if now - LAST_REQ.get(uid, 0) < REQUEST_COOLDOWN:
        return await m.reply(tr(L, "cooldown"))
    LAST_REQ[uid] = now

    target, via, err = await extract_target(client, m, L)
    if target is None:
        if err:
            return await m.reply(err, reply_markup=kb([home_btn(L)]))
        return await m.reply(tr(L, "nudge"), reply_markup=home_markup(uid, L))

    key = (uid, target)
    if now - RECENT.get(key, 0) < DUPLICATE_WINDOW:
        return await m.reply(tr(L, "duplicate"))
    RECENT[key] = now
    if len(RECENT) > 5000:
        RECENT.clear()

    await send_card(m, uid, target, L, via=via)


@app.on_callback_query()
async def on_callback(client, q: CallbackQuery):
    uid, data = q.from_user.id, q.data or ""
    L = get_lang(uid)

    async def edit(text, markup=None):
        try:
            await q.message.edit_text(text, reply_markup=markup)
        except Exception:
            pass

    if data.startswith(("adm:", "bc:")) and not is_owner(uid):
        return await q.answer(DENY_TEXT, show_alert=True)

    if data == "home":
        STATE.pop(uid, None)
        await edit(welcome_text(uid, q.from_user.first_name or ("صديقي" if L == "ar" else "friend"), L),
                   home_markup(uid, L))
    elif data == "help":
        await edit(help_text(L), kb([home_btn(L)]))
    elif data == "plan":
        text, markup = plan_view(uid, L)
        await edit(text, markup)

    elif data.startswith("setlang:"):
        new = data.split(":")[1]
        if new not in ("ar", "en"):
            return await q.answer(tr(L, "t_invalid"), show_alert=True)
        set_lang(uid, new)
        L = new
        await edit(welcome_text(uid, q.from_user.first_name or ("صديقي" if L == "ar" else "friend"), L),
                   home_markup(uid, L))
        return await q.answer(tr(L, "lang_set"))

    elif data == "myid":
        await q.answer()
        return await send_card(q.message, uid, uid, L, prefix=tr(L, "my_id"))

    elif data == "recent":
        text, markup = recent_view(uid, L)
        await edit(text, markup)

    elif data.startswith("rc:"):
        try:
            target = int(data.split(":")[1])
        except ValueError:
            return await q.answer(tr(L, "t_invalid"), show_alert=True)
        text, markup = build_card(uid, target, L, back="recent")
        await edit(text, markup)

    elif data.startswith(("m:", "pay:")):
        try:
            prefix, method, target = data.split(":")
            target = int(target)
            if method not in METHODS:
                raise ValueError
        except ValueError:
            return await q.answer(tr(L, "t_invalid"), show_alert=True)
        return await process_method(client, q, method, target, pay_intent=(prefix == "pay"))

    elif data.startswith("bad:"):
        try:
            op_id = int(data.split(":")[1])
        except ValueError:
            return await q.answer(tr(L, "t_invalid"), show_alert=True)
        return await handle_report(client, q, op_id)

    elif data == "subreq":
        if is_owner(uid) or sub_active(uid):
            return await q.answer(tr(L, "subreq_have"), show_alert=True)
        now = time.time()
        if now - SUBREQ.get(uid, 0) < SUBREQ_COOLDOWN:
            return await q.answer(tr(L, "subreq_wait"), show_alert=True)
        SUBREQ[uid] = now
        who = html.escape(q.from_user.first_name or "—")
        uname = f"@{q.from_user.username}" if q.from_user.username else "—"
        await notify_dev(
            client,
            f"📩 <b>طلب اشتراك جديد</b>\n{LINE}\n👤 {who}\n🏷 {uname}\n🆔 <code>{uid}</code>",
            kb([B(f"✅ تفعيل {SUB_DAYS} يوم", f"adm:subok:{uid}:{SUB_DAYS}", style="SUCCESS"),
                B("❌ رفض", f"adm:subno:{uid}", style="DANGER")]),
        )
        return await q.answer(tr(L, "subreq_sent"), show_alert=True)

    elif data.startswith("favs:"):
        text, markup = favs_view(uid, int(data.split(":")[1]), L)
        await edit(text, markup)

    elif data.startswith("fav:"):
        _, target, page = data.split(":")
        if not fav_get(uid, int(target)):
            return await q.answer(tr(L, "fav_missing"), show_alert=True)
        text, markup = build_card(uid, int(target), L, back=f"favs:{page}")
        await edit(text, markup)

    elif data.startswith("save:"):
        target = int(data.split(":")[1])
        if fav_get(uid, target):
            return await q.answer(tr(L, "fav_exists"), show_alert=True)
        if fav_count(uid) >= MAX_FAVS:
            return await q.answer(tr(L, "fav_full", max=MAX_FAVS), show_alert=True)
        STATE[uid] = {"mode": "alias", "target": target}
        await q.answer()
        await q.message.reply(tr(L, "alias_prompt", target=target))

    elif data.startswith("favdel:"):
        target = int(data.split(":")[1])
        await edit(
            tr(L, "fav_del_confirm", target=target),
            kb([B(tr(L, "btn_yes_del"), f"favdelok:{target}", style="DANGER"),
                B(tr(L, "btn_undo"), "favs:0", style="SUCCESS")]),
        )

    elif data.startswith("favdelok:"):
        fav_del(uid, int(data.split(":")[1]))
        await q.answer(tr(L, "fav_deleted"), show_alert=False)
        text, markup = favs_view(uid, 0, L)
        await edit(text, markup)

    elif data == "adm:home":
        STATE.pop(uid, None)
        await edit(ADMIN_TEXT, admin_markup())

    elif data == "adm:stats":
        await edit(stats_text(), kb([B("🔄 تحديث", "adm:stats", style="SUCCESS"),
                                      B("🔙 رجوع", "adm:home", style="PRIMARY")]))

    elif data == "adm:log":
        await edit(recent_ops_text(), kb([B("🔄 تحديث", "adm:log", style="SUCCESS"),
                                           B("🔙 رجوع", "adm:home", style="PRIMARY")]))

    elif data == "adm:pay":
        await edit(payments_text(), kb([B("🔄 تحديث", "adm:pay", style="SUCCESS"),
                                         B("🔙 رجوع", "adm:home", style="PRIMARY")]))

    elif data == "adm:subs":
        rows = db_exec("SELECT id,name,sub_until FROM users WHERE sub_until>? ORDER BY sub_until DESC LIMIT 30",
                       (now_ts(),), "all")
        body = "\n".join(f"• <code>{r['id']}</code> {_uname(r)} — حتى {fmt_ts(r['sub_until'], '%d/%m/%Y')}"
                         for r in rows) or "لا يوجد مشتركون حالياً."
        await edit(f"💎 <b>المشتركون</b>\n{LINE}\n{body}", BACK_ADMIN)

    elif data == "adm:banned":
        rows = db_exec("SELECT id,name FROM users WHERE banned=1 LIMIT 30", (), "all")
        body = "\n".join(f"• <code>{r['id']}</code> {_uname(r)}" for r in rows) or "لا يوجد محظورون ✨"
        await edit(f"📋 <b>قائمة المحظورين</b>\n{LINE}\n{body}", BACK_ADMIN)

    elif data in ("adm:ban", "adm:unban", "adm:unsub", "adm:ulog"):
        mode = data.split(":")[1]
        STATE[uid] = {"mode": mode}
        await q.answer()
        prompt = {
            "ban": "🆔 أرسل <b>أيدي</b> المستخدم المراد حظره 🚫",
            "unban": "🆔 أرسل <b>أيدي</b> المستخدم المراد فك حظره ✅",
            "unsub": "🆔 أرسل <b>أيدي</b> المستخدم المراد إلغاء اشتراكه 🔕",
            "ulog": "🆔 أرسل <b>أيدي</b> المستخدم لعرض سجل عملياته 🔎",
        }[mode]
        await q.message.reply(f"{prompt}\n(/cancel للإلغاء)")

    elif data == "adm:sub":
        STATE[uid] = {"mode": "sub"}
        await q.answer()
        await q.message.reply(
            "💎 <b>تفعيل اشتراك</b>\n"
            f"أرسل <b>الأيدي</b> فقط (اشتراك {SUB_DAYS} يوم)\n"
            "أو <b>الأيدي ثم عدد الأيام</b> مثل: <code>123456789 90</code>\n"
            "(يمكن التفعيل حتى لمن لم يبدأ البوت • /cancel للإلغاء)"
        )

    elif data.startswith("adm:subok:"):
        _, _, target, days = data.split(":")
        result = await activate_sub(client, int(target), int(days))
        await edit(result)

    elif data.startswith("adm:subno:"):
        target = int(data.split(":")[2])
        try:
            await client.send_message(target, tr(get_lang(target), "sub_rejected"))
        except Exception:
            pass
        await edit(f"❌ تم رفض طلب <code>{target}</code>.")

    elif data == "adm:bc":
        if BC["running"]:
            return await q.answer("⏳ هناك إذاعة جارية حالياً.", show_alert=True)
        STATE[uid] = {"mode": "bc"}
        await q.answer()
        await q.message.reply(
            "📢 <b>وضع الإذاعة</b>\n"
            "أرسل الآن الرسالة (نص / صورة / فيديو / ملف...) وسأعرض لك معاينة قبل الإرسال.\n"
            "(/cancel للإلغاء)"
        )

    elif data == "bc:go":
        st = STATE.get(uid)
        if not st or st.get("mode") != "bc_confirm":
            return await q.answer("⚠️ انتهت صلاحية العملية.", show_alert=True)
        if BC["running"]:
            return await q.answer("⏳ هناك إذاعة جارية.", show_alert=True)
        STATE.pop(uid, None)
        await q.answer("🚀 بدأت الإذاعة")
        await edit("📢 <b>جاري التحضير...</b>")
        asyncio.create_task(
            run_broadcast(client, q.message.chat.id, q.message.id, st["chat"], st["msg"])
        )

    elif data == "bc:abort":
        STATE.pop(uid, None)
        await edit("❌ تم إلغاء الإذاعة.", BACK_ADMIN)

    elif data == "bc:cancel":
        if BC["running"]:
            BC["cancel"] = True
            await q.answer("⛔ جاري الإيقاف...")
        else:
            await q.answer("لا توجد إذاعة جارية.", show_alert=True)


    else:
        return await q.answer()

    try:
        await q.answer()
    except Exception:
        pass


if __name__ == "__main__":
    log.info("🚀 Bot is starting... (colored buttons: %s)", "ON" if STYLES_OK else "OFF - install a Layer 224+ Pyrogram fork")
    try:
        app.run()
    except KeyboardInterrupt:
        log.info("🛑 Bot stopped.")
    except Exception as e:
        log.error("❌ فشل تشغيل البوت أو الاتصال بتيليجرام: %s", e)
        log.error("تحقق من صحة API_ID و API_HASH و BOT_TOKEN ومن اتصال الشبكة.")
        raise SystemExit(1)
