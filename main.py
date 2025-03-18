import os
import time
import subprocess
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ARIA2C_PATH = r"aria2-1.37.0-win-64bit-build1\aria2c.exe"

SAVE_PATH = "torrents"
os.makedirs(SAVE_PATH, exist_ok=True)
driver = webdriver.Chrome(ChromeDriverManager().install())


def magnet_to_torrent_aria2(magnet_link):
    print(f"🔄 Conversion du Magnet en .torrent : {magnet_link}")
    command = [
        ARIA2C_PATH,
        "--bt-metadata-only=true",
        "--bt-save-metadata=true",
        f"--dir={SAVE_PATH}",
        magnet_link
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  
    print(f"✅ Fichier .torrent enregistré dans {SAVE_PATH}")

for page in range(1, 46):
    url = f"https://getcomics.org/tag/marvel-now/page/{page}/"
    driver.get(url)
    time.sleep(2)

    articles = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'post-')]")

    for article in articles:
        try:
            article.click()
            time.sleep(3)

            try:
                magnet_link_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'magnet:?')]"))
                )
                magnet_link = magnet_link_element.get_attribute("href")

                if magnet_link:
                    print(f"🔗 Lien Magnet trouvé : {magnet_link}")
                    magnet_to_torrent_aria2(magnet_link)
                else:
                    print("⚠ Aucun lien Magnet trouvé.")

            except:
                print("⚠ Aucun lien Magnet trouvé.")

            driver.back()
            time.sleep(2)

        except Exception as e:
            print(f"❌ Erreur avec l'article : {e}")

driver.close()
