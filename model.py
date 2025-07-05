import time
import json
from datetime import datetime
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_rapido_fare(pickup, drop):
    pickup_encoded = quote(pickup)
    drop_encoded = quote(drop)
    url = f"https://m.rapido.bike/unup-home/seo/{pickup_encoded}/{drop_encoded}?version=v3"

    options = Options()
    options.add_argument("--headless=new") 
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    fare = "N/A"

    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-wrap")))
        cards = driver.find_elements(By.CLASS_NAME, "card-wrap")
        for card in cards:
            title = card.find_element(By.CLASS_NAME, "card-content").text.strip()
            price_text = card.find_elements(By.XPATH, "./div")[1].text.strip()
            if "Premium" in title:
                fare = price_text.split("-")[0].strip()
                break
    except Exception as e:
        print("❌ Rapido Error:", e)
    finally:
        driver.quit()

    return fare, url

def get_gobytaxi_fare(pickup, drop):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 30)
    fare = "N/A"

    try:
        driver.get("https://www.gobytaxi.com/asia/india")

        pickup_input = wait.until(EC.element_to_be_clickable((By.ID, "input_from")))
        pickup_input.clear()
        pickup_input.send_keys(pickup)
        time.sleep(1)
        pickup_input.send_keys(Keys.RETURN)

        drop_input = wait.until(EC.element_to_be_clickable((By.ID, "input_to")))
        drop_input.clear()
        drop_input.send_keys(drop)
        time.sleep(1)
        drop_input.send_keys(Keys.RETURN)

        go_btn = wait.until(EC.element_to_be_clickable((By.ID, "lets-go-button")))
        go_btn.click()
        print("Clicked LET'S GO")

        time.sleep(10)

        fare = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(),'INR')]/preceding-sibling::div")
        )).text.strip()

    except Exception as e:
        print("❌ GoByTaxi Error:", e)
    finally:
        driver.quit()

    return fare

def compare_and_save(pickup, drop):
    rapido_fare, rapido_url = get_rapido_fare(pickup, drop)
    gobytaxi_fare = get_gobytaxi_fare(pickup, drop)

    def clean_fare(value):
        return int(''.join(filter(str.isdigit, value))) if value and value != "N/A" else float('inf')

    r_fare_clean = clean_fare(rapido_fare)
    g_fare_clean = clean_fare(gobytaxi_fare)

    best = "No result"
    url = None
    if r_fare_clean < g_fare_clean:
        best = "Rapido (Cab Premium)"
        url = rapido_url
    elif g_fare_clean < r_fare_clean:
        best = "GoByTaxi"
        url = "https://www.gobytaxi.com/asia/india"

    result = {
        "pickup": pickup,
        "drop": drop,
        "rapido_cab_premium": rapido_fare,
        "gobytaxi": gobytaxi_fare,
        "best_option": best,
        "book_url": url,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("fare_comparison_result.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ Comparison complete. Result returned to app.")
    return result
