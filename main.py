from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import json
from dotenv import load_dotenv
load_dotenv()


class WellfoundMessenger:
    def __init__(self, cookies):
        self.driver = None
        self.cookies = cookies

    def initialize_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def check_login_status(self):
        try:
            # Wait for a few elements that indicate successful login
            time.sleep(3)
            # Check for multiple indicators of being logged in
            login_indicators = [
                "//div[contains(@class, 'UserAvatar')]",  # User avatar
                "//a[contains(@href, '/messages')]",  # Messages link
                "//div[contains(@class, 'UserMenu')]",  # User menu
            ]

            for indicator in login_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, indicator)
                    print(f"Found login indicator: {indicator}")
                    return True
                except:
                    continue

            # Also check if the login button is NOT present (another indication of being logged in)
            try:
                login_button = self.driver.find_element(
                    By.XPATH, "//a[contains(text(), 'Log in')]"
                )
                print("Login button found - not logged in")
                return False
            except:
                print("Login button not found - might be logged in")
                return True

            return False
        except Exception as e:
            print(f"Error checking login status: {str(e)}")
            return False

    def login_with_cookies(self):
        try:
            # First navigate to a page on the domain
            self.driver.get("https://wellfound.com")
            time.sleep(3)

            self.driver.delete_all_cookies()
            print("Deleted existing cookies")

            # Process and add each cookie
            for cookie in self.cookies:
                # Remove None values and unsupported keys
                cookie_dict = {
                    k: v
                    for k, v in cookie.items()
                    if v is not None
                    and k
                    in [
                        "domain",
                        "name",
                        "value",
                        "path",
                        "secure",
                        "httpOnly",
                        "expiry",
                    ]
                }

                # Convert expirationDate to expiry if exists
                if "expirationDate" in cookie:
                    cookie_dict["expiry"] = int(cookie["expirationDate"])

                print(f"Setting cookie: {cookie_dict['name']}")
                try:
                    self.driver.add_cookie(cookie_dict)
                except Exception as e:
                    print(f"Error setting cookie {cookie_dict['name']}: {str(e)}")
                time.sleep(0.5)

            print("Cookies set, refreshing page...")
            self.driver.get(
                "https://wellfound.com"
            )  # Full page load instead of refresh
            time.sleep(3)

            # Verify login status
            if self.check_login_status():
                print("Login verification successful!")
                return True
            else:
                print("Login verification failed!")
                # Get the current cookies for debugging
                current_cookies = self.driver.get_cookies()
                print("Current cookies after attempt:")
                for cookie in current_cookies:
                    print(f"Cookie {cookie['name']}: {cookie['value'][:20]}...")
                return False

        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False

    def send_message(self, recipient_url, message_text):
        try:
            # Navigate to recipient's profile
            self.driver.get(recipient_url)
            time.sleep(3)  # Wait for page load
            print(recipient_url)
            # Wait for and find message input
            message_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//textarea[@id="form-input--body"]')
                )
            )

            # Type and send message
            message_input.send_keys(message_text)
            time.sleep(1)

            send_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
            )
            send_btn.click()

            print("Message sent successfully!")
            return True

        except Exception as e:
            print(f"Error sending message: {str(e)}")
            # Take screenshot for debugging
            self.driver.save_screenshot("error_screenshot.png")
            print("Screenshot saved as error_screenshot.png")
            return False

    def close(self):
        if self.driver:
            self.driver.quit()


def main():
    # Your existing cookies array
    with open('cookies.json','r') as f:
        cookies = json.load(f)
    
    pprint(cookies)
    recipient_url = os.getenv('RECIPIENT_URL',"https://wellfound.com/jobs/messages/966023152")
    message_text = os.getenv('MESSAGE',"Task completed.")

    messenger = WellfoundMessenger(cookies)
    messenger.initialize_driver()

    try:
        if messenger.login_with_cookies():
            print("Logged in successfully with provided cookies")
            messenger.send_message(recipient_url, message_text)
        else:
            print("Failed to login with provided cookies")
            print("Attempting to capture current page source...")
            print(
                messenger.driver.page_source[:500] + "..."
            )
    finally:
        # input("Press Enter to close the browser...")
        messenger.close()


if __name__ == "__main__":
    main()
