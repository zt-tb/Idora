# Copyright (c) 2026 Mohsen Al-Taie (@K0_MG). See LICENSE (attribution required).
# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"متغير البيئة المطلوب '{name}' غير موجود أو فارغ. "
            f"أضفه في ملف .env محلياً أو في Variables على Railway."
        )
    return value


def _require_int(name: str) -> int:
    value = _require(name)
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(f"متغير البيئة '{name}' يجب أن يكون رقماً صحيحاً.")


API_ID = _require_int("API_ID")
API_HASH = _require("API_HASH")
BOT_TOKEN = _require("BOT_TOKEN")
DEVELOPER_ID = _require_int("DEVELOPER_ID")
DB_PATH = os.getenv("DB_PATH", "data/bot.db")

try:
    TZ_OFFSET = int(os.getenv("TZ_OFFSET_HOURS", "3"))
except ValueError:
    raise RuntimeError("متغير البيئة 'TZ_OFFSET_HOURS' يجب أن يكون رقماً صحيحاً.")
