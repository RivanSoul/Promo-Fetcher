# <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="30" height="30" alt="GitHub"> PromoFetcher

A powerful tool to automatically check and fetch promotional codes from Microsoft accounts, specifically targeting Xbox Game Pass offers. It includes built-in validation for Discord promo redemption.

## 🔗 Community & Support

> [!NOTE]
> Join our community regarding updates and support!

- **Telegram:** [t.me/meowleak](https://t.me/meowleak)

## ✨ Features

- **Multi-threaded:** Fast processing with configurable thread count (`MAX_THREADS`).
- **Auto-Login:** Handles Microsoft Live and Xbox authentication flows (User Token, XSTS).
- **Promo Detection:** Checks for specific Game Pass offer IDs.
- **Auto-Validation:** Validates found codes against Discord's API to ensure they are active and unused.
- **Proxy Support:** (Implied/Planned - currently uses direct requests or requires proxy config in requests if added).
## 📥 Installation

### Clone the Repository

```bash
git clone https://github.com/RivanSoul/PromoFetcher.git
cd PromoFetcher
```

### Install Dependencies

```bash
pip install requests colorama urllib3
```

## 🚀 Usage

1. **Setup Accounts:**
   Add your Microsoft accounts to `accs.txt` in the format:
   ```
   email:password
   email:password
   ```

2. **Configure Token:**
   Open `main.py` and replace `YOUR_DISCORD_TOKEN_HERE` with your actual Discord user token to enable code validation.

3. **Run:**
   ```bash
   python main.py
   ```

4. **Results:**
   - Working promos are saved to `promos.txt`.
   - Live stats are displayed in the console title.

## ⚠️ Disclaimer
This tool is for educational purposes only. Use it responsibly and at your own risk.

---

Modify with ❤️ by RivanSoul  
