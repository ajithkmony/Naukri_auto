import tkinter as tk
from tkinter import messagebox
import threading
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Use your logged-in Edge profile path here
EDGE_USER_DATA_DIR = r"C:\Users\admin\AppData\Local\Microsoft\Edge\User Data"
EDGE_PROFILE = "Default"  # Usually 'Default' unless you use multiple profiles

update_count = 0  # global counter

# UI update function
def update_counter_label():
    counter_label.config(text=f"Successful Updates: {update_count}")

def update_profile():
    global update_count
    try:
        edge_options = Options()
        edge_options.add_argument(f'--user-data-dir={EDGE_USER_DATA_DIR}')
        edge_options.add_argument(f'--profile-directory={EDGE_PROFILE}')

        driver = webdriver.Edge(options=edge_options)
        driver.get("https://www.naukri.com/mnjuser/profile")

        wait = WebDriverWait(driver, 30)

        # XPath for 'Update Profile' button
        update_btn_xpath = '//*[@id="root"]/div/div/span/div/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div/div[1]/em'
        
        try:
            update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, update_btn_xpath)))
            update_btn.click()
            print("Clicked 'Update Profile' button")
        except Exception as e:
            print(f"'Update Profile' button not found or not clickable: {e}")

        time.sleep(2)

        # XPath for 'Save' button
        save_btn_xpath = '//*[@id="saveBasicDetailsBtn"]'
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, save_btn_xpath)))
        save_btn.click()
        print("Clicked 'Save' button")

        update_count += 1
        update_counter_label()

        time.sleep(3)

    except Exception as e:
        print(f"Error during profile update: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

def start_scheduler(frequency_minutes):
    def job():
        while True:
            update_profile()
            print(f"Waiting {frequency_minutes} minutes for next update...")
            time.sleep(frequency_minutes * 60)

    thread = threading.Thread(target=job, daemon=True)
    thread.start()

def start():
    try:
        minutes = int(entry.get())
        if minutes <= 0:
            raise ValueError
        messagebox.showinfo("Started", f"Profile will update every {minutes} minutes.")
        start_scheduler(minutes)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of minutes.")

def reset_counter():
    global update_count
    update_count = 0
    update_counter_label()

# ---- GUI ----
root = tk.Tk()
root.title("Naukri Auto-Updater")

tk.Label(root, text="Update Frequency (minutes):").pack(padx=10, pady=5)

entry = tk.Entry(root)
entry.pack(padx=10, pady=5)
entry.insert(0, "60")  # default 60 minutes

tk.Button(root, text="Start Auto Update", command=start).pack(pady=10)

# Update Counter Display
counter_label = tk.Label(root, text="Successful Updates: 0", font=("Helvetica", 12))
counter_label.pack(pady=5)

# Reset Button
tk.Button(root, text="Reset Counter", command=reset_counter).pack(pady=5)

root.mainloop()
