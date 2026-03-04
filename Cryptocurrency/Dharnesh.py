import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_crypto_prices():
    # Setup browser
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment if you want background mode

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://coinmarketcap.com/")

    # Wait for table to load
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr")))

    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")

    data = []

    for row in rows[:10]:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) >= 8:
            data.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Coin": cols[2].text.replace("\n", " "),
                "Price": cols[3].text,
                "24h Change": cols[4].text,
                "Market Cap": cols[7].text
            })

    driver.quit()

    return pd.DataFrame(data)


def save_data(df):
    if df.empty:
        print("No data scraped.")
        return

    # Save CSV
    df.to_csv("crypto_prices.csv", index=False)

    # Save Excel with timestamp filename
    filename = f"crypto_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)

    print("Data saved successfully!")
    print("Rows scraped:", len(df))


if __name__ == "__main__":
    df = scrape_crypto_prices()
    print(df)
    save_data(df)