import cloudscraper
import json
import time
import random

def CheckPubgID(userid: str):
    """Check PUBG Mobile user ID using working proxy + cloudscraper method"""
    
    # Proxy credentials
    proxy_host = "gw.dataimpulse.com"
    proxy_port = "823"
    proxy_username = "0418c80a5bc7014e997f__cr.us"
    proxy_password = "5a6efe90fb1703fb"
    
    proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
    
    try:
        # Create cloudscraper session with proxy
        scraper = cloudscraper.create_scraper()
        scraper.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        # Enhanced headers that mimic real browser behavior
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://elitedias.com',
            'Pragma': 'no-cache',
            'Referer': 'https://elitedias.com/',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "game": "pubgm",
            "userid": userid
        }
        
        # First visit the main site to establish session
        print("Establishing session...")
        main_response = scraper.get('https://elitedias.com/', headers=headers, timeout=15)
        
        if main_response.status_code != 200:
            return {
                "status": "error",
                "error": f"Failed to establish session: HTTP {main_response.status_code}"
            }
        
        time.sleep(random.uniform(2, 4))
        
        # Make the API call
        print("Checking PUBG user ID...")
        response = scraper.post(
            "https://api.elitedias.com/checkid",
            headers=headers,
            json=payload,
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("valid") == "valid":
                return {
                    "status": "success",
                    "userid": userid,
                    "player_name": data.get("name", "Unknown"),
                    "openid": data.get("openid", "Unknown"),
                    "valid": True
                }
            else:
                return {
                    "status": "invalid",
                    "userid": userid,
                    "error": "User ID not found or invalid"
                }
        else:
            return {
                "status": "error",
                "error": f"API request failed: HTTP {response.status_code}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def main():
    print("=" * 60)
    print("           PUBG Mobile User ID Checker")
    print("=" * 60)
    print("Working version with proxy + cloudscraper bypass")
    print("=" * 60)
    
    while True:
        print("\nEnter a PUBG Mobile user ID (or 'quit' to exit):")
        user_input = input("User ID: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            print("Please enter a valid user ID.")
            continue
        
        print(f"\nChecking user ID: {user_input}")
        print("-" * 40)
        
        result = CheckPubgID(user_input)
        
        if result["status"] == "success":
            print("✅ VALID USER ID")
            print(f"Player Name: {result['player_name']}")
            print(f"OpenID: {result['openid']}")
        elif result["status"] == "invalid":
            print("❌ INVALID USER ID")
            print(f"Error: {result['error']}")
        else:
            print("❌ ERROR")
            print(f"Error: {result['error']}")
        
        print("-" * 40)

if __name__ == "__main__":
    main() 