import os
import time
import subprocess
import requests
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

for page in range(1, 1577):
    url = f"https://getcomics.org/tag/marvel-now/page/{page}/"
    driver.get(url)
    time.sleep(1)

    articles = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'post-')]")

    for article in articles:
        try:
            article.click()
            page_title = driver.title
            # Nettoyer le titre de la page (enlever les caractères spéciaux pour éviter des problèmes de nom de fichier)
            safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in page_title)
            time.sleep(1)

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
                    print('recherche CBR')
                    magnet_link_element =  WebDriverWait(driver, 10).until(
                             EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'aio-red') and contains(@title, 'DOWNLOAD NOW')]"))
                        )
                    cbr_url = magnet_link_element.get_attribute("href")
                    if cbr_url:
                        print(f"🔗 Fichier cbr trouvé : {cbr_url}")
                        response = requests.get(cbr_url, stream=True)
                        if response.status_code == 200:
                            timestamp = time.strftime("%Y%m%d-%H%M%S")
                            filename = os.path.join(SAVE_PATH, f"{safe_title}_{timestamp}.cbr")
                
                            with open(filename, "wb") as file:
                                for chunk in response.iter_content(1024):
                                    file.write(chunk)

                            print(f"✅ Fichier cbr enregistré dans {SAVE_PATH}")
                                    
                    else:
                            print("⚠ Aucun lien cbr trouvé.")

            except:
                print("⚠ Aucun lien Magnet trouvé.")
                
               

            driver.get(url)
            time.sleep(1)

        except Exception as e:
            print(f"❌ Erreur avec l'article : {e}")

driver.close()
