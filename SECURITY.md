# Security Policy

Please do not open a public issue for a vulnerability.

Report it privately to Mohsen Al-Taie on Telegram: [@K0_MG](https://t.me/K0_MG), or through GitHub's private vulnerability reporting on this repository.

Include the affected version, steps to reproduce and the impact.

## Built-in protections

- The admin panel and the `/refund` command work only for the `DEVELOPER_ID` account.
- User-controlled text shown in messages is HTML-escaped.
- Per-user request cooldown, duplicate-request window and a ban list.
- Star payments are validated in the pre-checkout step (currency and amount), and a failed delivery after payment is refunded automatically.
- `.env`, session files and the database files are ignored by Git; no secrets are stored in the repository.

If a bot token or `API_HASH` is ever exposed, revoke the token with [@BotFather](https://t.me/BotFather) immediately.
