from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service  # NEW IMPORT
import time


def run_mtn_sequence(driver, wait, short_wait, already_logged_in):
    print("\n--- INITIATING MTN DATA PROTOCOL ---")

    if not already_logged_in:
        print("3. Typing MTN credentials...")
        username_field = driver.find_element(By.ID, "txtUsr")
        password_field = driver.find_element(By.ID, "txtPwd")
        login_button = driver.find_element(By.ID, "btnLogin")

        username_field.send_keys("admin")
        password_field.send_keys("admin")
        login_button.click()
        print("Login button clicked successfully!")
        time.sleep(5)
    else:
        print("Already logged in! Skipping straight to USSD...")

    # --- MTN USSD NAVIGATION ---
    print("8. Looking for MTN USSD menu...")
    ussd_menu = wait.until(EC.element_to_be_clickable((By.ID, "menu_ussd")))
    time.sleep(2)

    ussd_menu.click()
    print("First click done...")
    time.sleep(2)

    ussd_menu.click()
    print("Second click done! USSD Menu opened.")
    time.sleep(2)

    print("9. Looking for USSD input...")
    ussd_input = wait.until(EC.visibility_of_element_located((By.ID, "USSD_send")))
    ussd_input.clear()

    # MTN Data Code
    mtn_code = "*323*1#"
    ussd_input.send_keys(mtn_code)

    print(f"10. Sending MTN code: {mtn_code}")
    send_button = driver.find_element(By.ID, "sendToNet")
    send_button.click()
    print("Success! Sent the code.")

    # --- MTN ERROR HANDLING ---
    print("Watching out for the annoying error to smash it...")
    try:
        ok_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "okbtn")))
        driver.execute_script("arguments[0].click();", ok_button)
        print("Error pop-up smashed instantly!")
    except TimeoutException:
        print("No error pop-up appeared.")


def run_airtel_sequence(driver, wait, short_wait, already_logged_in):
    print("\n--- INITIATING AIRTEL DATA PROTOCOL ---")

    if not already_logged_in:
        print("3. Typing Airtel password...")
        password_field = driver.find_element(By.ID, "txtPwd")
        password_field.send_keys("admin")

        # Simulating the Enter key for Airtel
        password_field.send_keys(Keys.RETURN)
        print("Hit ENTER to log in!")
        time.sleep(2)
    else:
        print("Already logged in! Skipping straight to USSD...")

    # --- AIRTEL USSD NAVIGATION ---
    print("8. Clicking Advanced Settings...")
    adv_settings = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#sleep_mode']")))
    adv_settings.click()
    time.sleep(1)

    print("Looking for Airtel USSD menu...")
    ussd_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#ussd']")))
    time.sleep(1)

    ussd_menu.click()
    print("USSD Menu clicked and opened.")
    time.sleep(1)

    print("9. Looking for USSD input...")
    ussd_input = wait.until(EC.visibility_of_element_located((By.ID, "USSD_send")))
    ussd_input.clear()

    # Airtel Data Code
    airtel_code = "*323*1#"
    ussd_input.send_keys(airtel_code)

    print(f"10. Sending Airtel code: {airtel_code}")
    send_button = driver.find_element(By.ID, "sendToNet")
    send_button.click()
    print("Success! Sent the Airtel code.")

    # --- AIRTEL ERROR HANDLING ---
    print("Watching out for the annoying error to smash it...")
    try:
        ok_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "okbtn")))
        driver.execute_script("arguments[0].click();", ok_button)
        print("Error pop-up smashed instantly!")
    except TimeoutException:
        print("No error pop-up appeared.")


def master_router_bot():
    print("Initiating Master Auto-Detect Router Bot...")

    # --- NEW OFFLINE LAUNCHER ---
    print("Loading local ChromeDriver from Downloads folder...")

    # See how it has the extra folder name in the middle now?
    my_service = Service(executable_path=r"D:\PycharmProjects\PythonProject2\chromedriver.exe")
    driver = webdriver.Chrome(service=my_service)

    wait = WebDriverWait(driver, 10)
    short_wait = WebDriverWait(driver, 4)

    try:
        print("1. Loading dashboard (http://192.168.0.1)...")
        driver.get("http://192.168.0.1")

        print("2. Scanning HTML to identify the network...")
        network = "UNKNOWN"
        logged_in = False

        # --- DETECTION PHASE ---
        try:
            short_wait.until(EC.presence_of_element_located((By.ID, "txtPwd")))

            try:
                driver.find_element(By.ID, "txtUsr")
                network = "MTN"
            except:
                network = "AIRTEL"

            logged_in = False

        except TimeoutException:
            try:
                short_wait.until(EC.presence_of_element_located((By.ID, "menu_ussd")))
                network = "MTN"
                logged_in = True
            except TimeoutException:
                try:
                    # UPDATED: Now looks for Advanced Settings to identify Airtel when logged in
                    short_wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='#sleep_mode']")))
                    network = "AIRTEL"
                    logged_in = True
                except TimeoutException:
                    pass

        # --- ROUTING PHASE ---
        if network == "UNKNOWN":
            print("\n❌ Could not identify the router. Are you sure you are connected to the WiFi?")
            return

        print(f"\n✅ DETECTED: {network} Router! (Already Logged In: {logged_in})")

        if network == "MTN":
            run_mtn_sequence(driver, wait, short_wait, logged_in)
        elif network == "AIRTEL":
            run_airtel_sequence(driver, wait, short_wait, logged_in)

        print("\n11. Waiting 30 seconds to let the network finish before closing...")
        time.sleep(30)

    except Exception as e:
        print(f"\nBOT CRASHED! Error details: {e}")

    finally:
        driver.quit()
        print("Browser closed. Automation complete!")


if __name__ == "__main__":
    master_router_bot()