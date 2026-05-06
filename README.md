# PromoFetcher

A high-speed asynchronous tool to check Microsoft/Xbox accounts for Game Pass promotions and validate them using Discord's API.


## 🔗 Community & Support

> [!NOTE]
> Join our community regarding updates and support!

- **Telegram:** [t.me/meowleak](https://t.me/meowleak)
- **Discord:** [https://discord.gg/7RRv93nXCp](https://discord.gg/D3FG34BFjS)


## Features
- **Dynamic Offer Fetching**: Automatically loops through all available Game Pass perks instead of relying on a single hardcoded offer ID. Prevents the script from breaking when Xbox updates their promotional campaigns.
- **Claimed Promo Recovery**: Safely extracts Discord promo links even from accounts where the promo was already previously "claimed" or generated.
- **Fast Checking**: Uses multi-threading (up to 100 threads) for rapid account processing.
- **Xbox Authentication**:  Handles full authentication flow for Xbox Live services.
- **Promo Validation**: Automatically verifies found promo codes against Discord's entitlement API (checks claims, max claims, and expiration limits).
- **Live Stats**: Real-time console title updates showing progress.

## Prerequisites
- Python 3.x
- `curl_cffi`
- `colorama`

## Installation

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Discord Token Setup
**IMPORTANT**: You must use your own Discord token for promo validation to work. The validation uses the Discord API to check if a promo code is still valid, claimed, or expired.

1. Open `main.py` in a text editor
2. Find line 30 where `DISCORD_TOKEN` is defined
3. Replace the existing token with your own Discord token:
   ```python
   DISCORD_TOKEN = "YOUR_DISCORD_TOKEN_HERE"
   ```

To get your Discord token:
- Open Discord in your browser
- Press `F12` to open Developer Tools
- Go to the `Console` tab
- Type: `(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()`
- Copy the token (without quotes)

> [!WARNING]
> Never share your Discord token with anyone. Keep it private and secure.

## Usage

1. **Prepare Accounts**:
   Add your Microsoft accounts to a file named `accs.txt` in the same directory. The format must be:
   ```text
   email:password
   email2:password
   ```

2. **Run the Script**:
   ```bash
   python main.py
   ```

3. **Output**:
   - Working promos are printed to the console and saved to `promos.txt` automatically.
   - The file format for saved promos includes usage stats and expiry information.

## Advanced Tweaks
- You can adjust `MAX_THREADS` in `main.py` (Default: 100) to suit your system's capabilities or prevent rate-limits on your network.

## Disclaimer
This tool is for educational purposes only. Use responsibly.

---
Modify with ❤️ by RivanSoul
