from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 1. Set up Chrome Options
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\HP PAVILION\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument(r"profile-directory=Profile 1")

# 2. The Balanced Anti-Crash Armor
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--hide-crash-restore-bubble")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("detach", True)

# --- THE NEW OVERRIDE ---
# Tell Selenium to stop waiting for the Google homepage to fully load!
chrome_options.page_load_strategy = 'eager'
# ------------------------

print("Launching browser with your lightweight Eze profile...")
driver = webdriver.Chrome(options=chrome_options)

# Give the connection a brief moment to stabilize
time.sleep(2)

# 3. Go directly to the form
print("Forcing navigation to the Google Form...")
driver.get("https://docs.google.com/forms/d/e/1FAIpQLScBzjfFOtBtrjWbTzGNhg1RJpraukjReiH4QoDZjJhn9KdqqA/viewform?usp=publish-editor")

# Give the form time to load
time.sleep(5)

print("Bot has entered the form successfully!")
