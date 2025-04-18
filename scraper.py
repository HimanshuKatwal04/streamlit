from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_swiggy_results(query, pin_code):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.swiggy.com/")
        time.sleep(3)

        location_input = driver.find_element(By.ID, "location")
        location_input.send_keys(pin_code)
        time.sleep(3)

        suggestions = driver.find_elements(By.CLASS_NAME, "_3lmRa")
        if suggestions:
            suggestions[0].click()
        time.sleep(5)

        search_btn = driver.find_element(By.CLASS_NAME, "_1fiQt")
        search_btn.click()
        time.sleep(2)

        search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search for restaurants and food']")
        search_box.send_keys(query)
        time.sleep(3)

        driver.find_element(By.CLASS_NAME, "_3iFC5").click()
        time.sleep(5)

        items = driver.find_elements(By.CLASS_NAME, "_2wg_t")
        results = []
        for item in items:
            name = item.find_element(By.CLASS_NAME, "nA6kb").text
            price = item.find_element(By.CLASS_NAME, "_1W_TH").text if item.find_elements(By.CLASS_NAME, "_1W_TH") else "N/A"
            results.append({
                "name": name,
                "price": price,
                "location": f"Near {pin_code}",
                "rating": "N/A",
                "url": driver.current_url
            })
        return results

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        driver.quit()
