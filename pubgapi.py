import cloudscraper
import json
import time
import concurrent.futures
from typing import List, Dict

class FastPubgChecker:
    def __init__(self):
        # Proxy credentials
        self.proxy_host = "80.71.152.7"
        self.proxy_port = "5433"
        self.proxy_username = "OC9OST24KYWD"
        self.proxy_password = "Y8ALT51FX100"
        self.proxy_url = f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}"
        
        # Create a persistent scraper session for reuse
        self.scraper = cloudscraper.create_scraper()
        self.scraper.proxies = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }
        
        # Optimized headers
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Origin': 'https://elitedias.com',
            'Referer': 'https://elitedias.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/json'
        }
        
        # Session established flag
        self.session_established = False
    
    def establish_session_once(self):
        """Establish session only once and reuse it"""
        if not self.session_established:
            try:
                print("Establishing session (one-time setup)...")
                response = self.scraper.get('https://elitedias.com/', headers=self.headers, timeout=10)
                if response.status_code == 200:
                    self.session_established = True
                    print("Session established successfully!")
                else:
                    print(f"Warning: Session establishment returned {response.status_code}")
            except Exception as e:
                print(f"Warning: Session establishment failed: {e}")
    
    def check_single_userid(self, userid: str) -> Dict:
        """Check a single user ID with minimal overhead"""
        try:
            # Ensure session is established
            if not self.session_established:
                self.establish_session_once()
            
            payload = {
                "game": "pubgm",
                "userid": userid
            }
            
            # Make the API call with reduced timeout
            response = self.scraper.post(
                "https://api.elitedias.com/checkid",
                headers=self.headers,
                json=payload,
                timeout=8  # Even faster timeout
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
                    "userid": userid,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "userid": userid,
                "error": str(e)
            }
    
    def check_multiple_userids(self, userids: List[str]) -> List[Dict]:
        """Check multiple user IDs in parallel using ThreadPoolExecutor"""
        print(f"Checking {len(userids)} user IDs in parallel...")
        
        # Establish session once before parallel processing
        self.establish_session_once()
        
        results = []
        # Increased max_workers for faster processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all tasks
            future_to_userid = {executor.submit(self.check_single_userid, userid): userid for userid in userids}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_userid):
                result = future.result()
                results.append(result)
                print(f"✓ {result['userid']}: {result['status']}")
        
        return results

def main():
    print("=" * 60)
    print("           FAST PUBG Mobile User ID Checker")
    print("=" * 60)
    print("Optimized for speed with parallel processing")
    print("=" * 60)
    
    checker = FastPubgChecker()
    
    while True:
        print("\nChoose mode:")
        print("1. Single user ID check (ultra-fast)")
        print("2. Multiple user IDs (parallel - fastest)")
        print("3. Batch from file")
        print("4. Quit")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "4":
            print("Goodbye!")
            break
        
        elif choice == "1":
            userid = input("Enter user ID: ").strip()
            if userid:
                start_time = time.time()
                result = checker.check_single_userid(userid)
                end_time = time.time()
                
                print(f"\nResult (took {end_time - start_time:.2f}s):")
                print("-" * 40)
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
        
        elif choice == "2":
            print("Enter user IDs (one per line, empty line to finish):")
            userids = []
            while True:
                userid = input().strip()
                if not userid:
                    break
                userids.append(userid)
            
            if userids:
                start_time = time.time()
                results = checker.check_multiple_userids(userids)
                end_time = time.time()
                
                print(f"\nResults (took {end_time - start_time:.2f}s for {len(userids)} IDs):")
                print(f"Average time per ID: {(end_time - start_time)/len(userids):.2f}s")
                print("-" * 40)
                for result in results:
                    if result["status"] == "success":
                        print(f"✅ {result['userid']}: {result['player_name']}")
                    elif result["status"] == "invalid":
                        print(f"❌ {result['userid']}: Invalid")
                    else:
                        print(f"❌ {result['userid']}: Error - {result['error']}")
                print("-" * 40)
        
        elif choice == "3":
            filename = input("Enter filename with user IDs (one per line): ").strip()
            try:
                with open(filename, 'r') as f:
                    userids = [line.strip() for line in f if line.strip()]
                
                if userids:
                    print(f"Loaded {len(userids)} user IDs from {filename}")
                    start_time = time.time()
                    results = checker.check_multiple_userids(userids)
                    end_time = time.time()
                    
                    print(f"\nResults (took {end_time - start_time:.2f}s for {len(userids)} IDs):")
                    print(f"Average time per ID: {(end_time - start_time)/len(userids):.2f}s")
                    print("-" * 40)
                    
                    # Save results to file
                    output_filename = f"results_{int(time.time())}.json"
                    with open(output_filename, 'w') as f:
                        json.dump(results, f, indent=2)
                    
                    print(f"Results saved to {output_filename}")
                    print("-" * 40)
                else:
                    print("No user IDs found in file")
            except FileNotFoundError:
                print(f"File {filename} not found")
            except Exception as e:
                print(f"Error reading file: {e}")

if __name__ == "__main__":
    main() 