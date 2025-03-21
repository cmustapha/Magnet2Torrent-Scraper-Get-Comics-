import os
import time
import traceback
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

ARIA2C_PATH = r"aria2-1.37.0-win-64bit-build1\aria2c.exe"

SAVE_PATH = "torrents"
PROGRESS_FILE = "progress.txt"
os.makedirs(SAVE_PATH, exist_ok=True)

# Fonction pour récupérer la dernière page traitée
def get_last_page():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            pass
    return 1  # Par défaut, commencer à la première page

# Fonction pour enregistrer la dernière page traitée
def save_last_page(page):
    with open(PROGRESS_FILE, "w") as file:
        file.write(str(page))

# Configuration du driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Reprendre depuis la dernière page traitée
start_page = get_last_page()

def magnet_to_torrent_aria2(magnet_link):
    print(f"🔄 Enregistrement du Magnet URL : {magnet_link}")

    magnet_file_path = f"{SAVE_PATH}/magnet_links.txt"
    with open(magnet_file_path, "a", encoding="utf-8") as file:
        file.write(magnet_link + "\n")

    print(f"✅ URL  magnet enregistré dans {magnet_file_path}")

def save_cbr(magnet_link):
    print(f"🔄 Enregistrement du cbr URL : {magnet_link}")

    magnet_file_path = f"{SAVE_PATH}/cbr_links.txt"
    with open(magnet_file_path, "a", encoding="utf-8") as file:
        file.write(magnet_link + "\n")

    print(f"✅ URL cbr  enregistré dans {magnet_file_path}")
# Boucle à travers les pages
for page in range(start_page, 1577):
    print(f"📄 Traitement de la page {page}")
    url = f"https://getcomics.org/page/{page}/"
    driver.get(url)
    time.sleep(5)
    section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.page-contents.post-list.post-list-masonry"))
        )

    articles = section.find_elements(By.TAG_NAME, "article")
    print(f"🔍 {len(articles)} articles trouvés sur cette page.")

    for article in articles:
        try:
            article.click()
            time.sleep(5)

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
                    print("⚠ Recherche CBR.")
                    try:
                            magnet_link_element =  WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'aio-red') and contains(@title, 'DOWNLOAD NOW')]"))
                                    )
                            cbr_url = magnet_link_element.get_attribute("href")

                            if cbr_url:

                                    print(f"🔗 Lien Magnet trouvé : {cbr_url}")
                                    save_cbr(cbr_url)
            
                                    print(f"✅ Lien Fichier cbr")
                                
                            else:
                                print("⚠ Aucun lien cbr trouvé.")

                    except:
                            print("⚠ Aucun lien cbr trouvé.")
            except:
                print("⚠ Aucun lien Magnet trouvé.")
                print("⚠ Recherche CBR.")
                try:
                            magnet_link_element =  WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'aio-red') and contains(@title, 'DOWNLOAD NOW')]"))
                                    )
                            cbr_url = magnet_link_element.get_attribute("href")

                            if cbr_url:

                                    print(f"🔗 Lien cbr trouvé : {cbr_url}")
                                    save_cbr(cbr_url)
            
                                    print(f"✅ Lien cbr enregistrée ")
                                
                            else:
                                print("⚠ Aucun lien cbr trouvé.")

                except:
                            print("⚠ Aucun lien cbr trouvé.")
            driver.back()
            time.sleep(5)

        except Exception as e:
            print(f"❌ Erreur avec un article : {traceback.format_exc()}")

    # Sauvegarde de la progression
    save_last_page(page)
    print(f"✅ Progression sauvegardée : page {page}")

driver.close()
