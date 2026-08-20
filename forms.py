import subprocess
import time
import pyperclip
import pyautogui

# 1. Put the link directly into your computer's clipboard
form_link = "https://docs.google.com/forms/d/e/1FAIpQLScBzjfFOtBtrjWbTzGNhg1RJpraukjReiH4QoDZjJhn9KdqqA/viewform?usp=publish-editor"
pyperclip.copy(form_link)

# 2. Launch your Chrome profile
print("Launching Chrome...")
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
subprocess.Popen([chrome_path, "--profile-directory=Profile 1"])

# Give Chrome a few seconds to appear and highlight the search bar
time.sleep(3)

# 3. Just press Ctrl+V and Enter!
print("Pasting the link...")
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')

print("Form is loading!")