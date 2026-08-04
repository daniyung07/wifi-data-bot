from flask import Flask, render_template_string, request
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)

# --- HTML INTERFACE ---
# --- HTML INTERFACE ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Router Bot</title>
</head>
<body style="text-align:center; padding-top:100px; font-family:Arial; background-color:#222; color:white;">
    <h2>Wi-Fi Data Bot</h2>
    <form action="/run-bot" method="POST">

        <select name="ussd_code" onchange="this.form.submit()" style="padding:15px; font-size:20px; width:80%; max-width:300px; border-radius:10px; border:none; margin-bottom:20px; text-align:center; font-weight:bold;">
            <option value="" disabled selected>Tap to select a command...</option>
            <option value="*323*1#">*323*1#</option>
            <option value="*671*200*1#">*671*200*1#</option>
            <option value="*939*77#">*939*77#</option>
            <option value="*310#">*310#</option>
        </select>

    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)


@app.route('/run-bot', methods=['POST'])
def trigger_bot():
    user_input_code = request.form.get('ussd_code')
    print(f"Phone pressed the button! Code: {user_input_code}")
    threading.Thread(target=master_router_bot, args=(user_input_code,)).start()
    return "<h2 style='text-align:center; padding:50px; font-family:Arial;'>Command Sent! Look at your laptop screen.</h2>"


# --- NEW REUSABLE FUNCTION ---
def handle_continuous_code(driver, wait, ussd_code):
    # MULTI-STEP LOGIC
    if ussd_code == "*939*77#":
        print("11. Waiting for continuous menu to load...")
        time.sleep(8)

        print("12. Typing option 3...")
        ussd_input = wait.until(EC.visibility_of_element_located((By.ID, "USSD_send")))
        ussd_input.clear()
        ussd_input.send_keys("3")
        driver.find_element(By.ID, "sendToNet").click()

        print("13. Waiting for password prompt...")
        time.sleep(8)

        print("14. Typing password 1230...")
        ussd_input = wait.until(EC.visibility_of_element_located((By.ID, "USSD_send")))
        ussd_input.clear()
        ussd_input.send_keys("1230")
        driver.find_element(By.ID, "sendToNet").click()
        print("Success! Continuous code finished.")

    # ERROR HANDLING
    try:
        ok_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "okbtn")))
        driver.execute_script("arguments[0].click();", ok_button)
        print("Error pop-up smashed instantly!")
    except TimeoutException:
        pass


# --- SELENIUM BOT ---
def run_mtn_sequence(driver, wait, short_wait, already_logged_in, ussd_code):
    print("\n--- INITIATING MTN DATA PROTOCOL ---")
    if not already_logged_in:
        print("3. Typing MTN credentials...")
        username_field = driver.find_element(By.ID, "txtUsr")
        password_field = driver.find_element(By.ID, "txtPwd")
        login_button = driver.find_element(By.ID, "btnLogin")
        username_field.send_keys("admin")
        password_field.send_keys("admin")
        login_button.click()
        time.sleep(5)
    else:
        print("Already logged in! Skipping straight to USSD...")

    print("8. Looking for MTN USSD menu...")
    ussd_menu = wait.until(EC.element_to_be_clickable((By.ID, "menu_ussd")))
    time.sleep(2)
    ussd_menu.click()
    time.sleep(2)
    ussd_menu.click()
    time.sleep(2)

    print("9. Looking for USSD input...")
    ussd_input = wait.until(EC.visibility_of_element_located((By.ID, "USSD_send")))
    ussd_input.clear()
    ussd_input.send_keys(ussd_code)

    print(f"10. Sending initial code: {ussd_code}")
    send_button = driver.find_element(By.ID, "sendToNet")
    send_button.click()

    # Call the reusable function right here
    handle_continuous_code(driver, wait, ussd_code)


def run_airtel_sequence(driver, wait, short_wait, already_logged_in, ussd_code):
    print("\n--- INITIATING AIRTEL DATA PROTOCOL ---")
    if not already_logged_in:
        print("3. Typing Airtel password...")
        password_field = driver.find_element(By.ID, "txtPwd")
        password_field.send_keys("admin")
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
    else:
        print("Already logged in! Skipping straight to USSD...")

    print("8. Clicking Advanced Settings...")
    adv_settings = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#sleep_mode']")))
    adv_settings.click()
    time.sleep(2)

    print("Looking for Airtel USSD menu...")
    ussd_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#ussd']")))
    time.sleep(1)
    ussd_menu.click()
    time.sleep(2)

    print("9. Looking for USSD input...")
    ussd_input = wait.until(EC.visibility_of_element_located((By.ID, "USSD_send")))
    ussd_input.clear()
    ussd_input.send_keys(ussd_code)

    print(f"10. Sending initial code: {ussd_code}")
    send_button = driver.find_element(By.ID, "sendToNet")
    send_button.click()

    # Call the reusable function right here too
    handle_continuous_code(driver, wait, ussd_code)


def master_router_bot(ussd_code):
    print("Initiating Master Auto-Detect Router Bot...")
    my_service = Service(executable_path=r"D:\PycharmProjects\PythonProject2\chromedriver.exe")
    driver = webdriver.Chrome(service=my_service)
    wait = WebDriverWait(driver, 10)
    short_wait = WebDriverWait(driver, 4)

    try:
        driver.get("http://192.168.0.1")
        network = "UNKNOWN"
        logged_in = False

        try:
            short_wait.until(EC.presence_of_element_located((By.ID, "txtPwd")))
            try:
                driver.find_element(By.ID, "txtUsr")
                network = "MTN"
            except:
                network = "AIRTEL"
        except TimeoutException:
            try:
                short_wait.until(EC.presence_of_element_located((By.ID, "menu_ussd")))
                network = "MTN"
                logged_in = True
            except TimeoutException:
                try:
                    short_wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='#sleep_mode']")))
                    network = "AIRTEL"
                    logged_in = True
                except TimeoutException:
                    pass

        if network == "UNKNOWN":
            print("\n❌ Could not identify the router. Are you sure you are connected to the WiFi?")
            return

        print(f"\n✅ DETECTED: {network} Router! (Already Logged In: {logged_in})")
        if network == "MTN":
            run_mtn_sequence(driver, wait, short_wait, logged_in, ussd_code)
        elif network == "AIRTEL":
            run_airtel_sequence(driver, wait, short_wait, logged_in, ussd_code)

        time.sleep(30)

    except Exception as e:
        print(f"\nBOT CRASHED! Error details: {e}")
    finally:
        driver.quit()
        print("Browser closed. Automation complete!")


if __name__ == "__main__":
    print("Web Server running! Connect your phone to the Wi-Fi.")
    app.run(host='0.0.0.0', port=5000)