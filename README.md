<div align="center">

# Idora

**Telegram bot that finds a person and shows their account info from a Telegram user ID.**

English · [العربية](README.ar.md)

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

> **Open source with attribution.** Idora is released under the MIT License with an attribution requirement. You may use, modify and share it, but you must keep the [NOTICE](NOTICE) file and the copyright headers, and credit the original author, **Mohsen Al-Taie (@K0_MG)**. See [LICENSE](LICENSE).

## What it does

You send the bot a Telegram **user ID**. It replies with a card for that account and six buttons. Each button gives you a different way to open the person's account or see their info.

Everything starts from the ID. If you don't have the number, you can send a username, a forwarded message or a contact instead, and the bot converts it to the ID first.

| Method | What you get |
|---|---|
| 💬 **Direct chat** | A button that opens a chat with the account (`tg://openmessage?user_id=...`) |
| 👤 **Profile** | A button that opens the profile (`tg://user?id=...`) |
| 🌐 **Username link** | The account's `t.me/username` link, if it has a public username |
| 🖥 **Telegram Web** | A button that opens the account in Telegram Web |
| 🔍 **Account info** | Name, username, bio and flags such as Premium, bot, verified, scam or fake, when Telegram exposes them to the bot |
| 🖼 **Profile photo** | The account's profile photo, if it has one the bot can see |

Direct chat, profile and Telegram Web are links that open inside your Telegram app. Whether they open depends on Telegram: if your app has never seen that account, the link may not work. That is what the **"❌ Link did not work"** button is for (see below).

## How to use it

1. Open the bot on Telegram and send `/start`.
2. Send the person's numeric **user ID**, for example `123456789` (Arabic and Persian digits work too).
   - No ID at hand? These are converted to the ID automatically: a username (`@username` or a `t.me/username` link), a `tg://user?id=123456789` link, a message **forwarded** from the person, or a shared **contact**.
3. Pick a method from the buttons on the card.
4. The result arrives in the chat. You can save the account to your favorites with an alias.

You can also open a card directly: add `?start=` followed by an ID to the bot's link (for example `?start=123456789`) and the card for that ID opens.

## Free trial, Stars and subscription

- Every user gets **one free trial**.
- After that, each use costs **1 Telegram Star**, or you can have a **30-day subscription** with no per-use charge.
- Payments use Telegram Stars (`XTR`), so no payment provider is needed.
- **A use that returns no result is not counted.** If there is no username, no photo or no info, or sending fails, the free trial is restored or no Star is charged.
- **"❌ Link did not work"** appears under the chat, profile and Telegram Web results. It restores the free trial or refunds the Star automatically, up to 3 reports per user, and notifies the developer.
- If delivery fails after a payment, the payment is refunded automatically.
- Users can press **Request subscription**; the developer gets a notification with an activate button.

## Commands

| Command | Purpose |
|---|---|
| `/start` | Main menu: my ID, recent IDs, favorites, my plan, help, language |
| `/help` | Usage guide |
| `/favs` | Saved accounts with aliases (up to 30) |
| `/plan` | Your free trial, Stars price and subscription status |
| `/lang` | Switch between Arabic and English |
| `/paysupport` | Your latest payments and a button to contact the developer |
| `/cancel` | Cancel the current step |
| `/admin` | Developer panel (developer only) |
| `/refund USER_ID CHARGE_ID` | Refund a Star payment (developer only) |

The language is chosen automatically from the user's Telegram language, and can be changed with `/lang`.

## Developer panel

`/admin` opens a panel, available only to the account in `DEVELOPER_ID`:

- Statistics, subscribers list, operation log and per-user log
- Payments list
- Activate or cancel a subscription (default 30 days, or `USER_ID DAYS`)
- Broadcast to all users with a preview, confirmation and progress bar
- Ban, unban and list banned users

Everything is stored in a local SQLite database: users, favorites, operations, free trials and payments.

## Setup

**Requirements:** Python 3.11 or newer, `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org), a bot token from [@BotFather](https://t.me/BotFather), and your own Telegram user ID.

| Variable | Required | Description |
|---|---|---|
| `API_ID` / `API_HASH` | Yes | From my.telegram.org |
| `BOT_TOKEN` | Yes | From @BotFather |
| `DEVELOPER_ID` | Yes | Your Telegram ID. The only account allowed to use the developer panel |
| `DB_PATH` | No | Database path. Default `data/bot.db` |
| `TZ_OFFSET_HOURS` | No | Time zone offset used to show times. Default `3` |

Run it locally:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then put your real values in .env
python main.py
```

Deploy on Railway:

1. Push the project to a GitHub repository (never commit `.env`).
2. In Railway choose **New Project → Deploy from GitHub repo**.
3. Add `API_ID`, `API_HASH`, `BOT_TOKEN` and `DEVELOPER_ID` under **Variables**.
4. **Important:** create a **Volume**, mount it on `/app/data`, and set `DB_PATH=/app/data/bot.db`. Without it, subscriptions, payments and logs are wiped on every deploy.
5. Check the logs for `Bot is starting`, then send `/start`.

## Project layout

| File | Purpose |
|---|---|
| `main.py` | Bot logic, payments, favorites and developer panel |
| `i18n.py` | All user-facing text in Arabic and English |
| `config.py` | Reads settings from environment variables |
| `Procfile`, `railway.json`, `runtime.txt` | Deployment settings (worker, Python 3.11) |

The price (`STAR_PRICE`), free trials (`FREE_TRIALS`), subscription length (`SUB_DAYS`) and limits are constants at the top of `main.py`.

## Privacy and security

Idora only shows what Telegram lets a bot see about an account. It does not read private chats or reveal phone numbers. Use it responsibly and respect other people's privacy. See [SECURITY.md](SECURITY.md) for how to report a vulnerability. Never share your bot token or `API_HASH`.

## Credit

If you use Idora or build on it, please credit the author in your README or bot description, for example: *Based on Idora by Mohsen Al-Taie (@K0_MG)*. Redistributions must keep the `NOTICE` file.

To cite it in research or documentation, use [CITATION.cff](CITATION.cff) (GitHub shows a "Cite this repository" button).

## Author

**Mohsen Al-Taie**

<div align="center">

<img src="assets/divider.svg" width="100%" alt="" />

### 📱 Follow Me | تابعني

<div dir="ltr">

<a href="https://t.me/K0_MG"><img src="assets/social/telegram.svg" width="72" alt="Telegram @K0_MG" /></a>
<a href="https://instagram.com/z0_28"><img src="assets/social/instagram.svg" width="72" alt="Instagram z0_28" /></a>
<a href="https://www.tiktok.com/@zt_tb"><img src="assets/social/tiktok.svg" width="72" alt="TikTok @zt_tb" /></a>
<a href="https://youtube.com/@M7JN"><img src="assets/social/youtube.svg" width="72" alt="YouTube @M7JN" /></a>
<a href="https://github.com/zt-tb"><img src="assets/social/github.svg" width="72" alt="GitHub zt-tb" /></a>

</div>

[Telegram @K0_MG](https://t.me/K0_MG) · [Instagram z0_28](https://instagram.com/z0_28) · [TikTok @zt_tb](https://www.tiktok.com/@zt_tb) · [YouTube @M7JN](https://youtube.com/@M7JN) · [GitHub zt-tb](https://github.com/zt-tb)

<img src="assets/divider.svg" width="100%" alt="" />

</div>

Copyright (c) 2026 Mohsen Al-Taie (@K0_MG). See [LICENSE](LICENSE).
