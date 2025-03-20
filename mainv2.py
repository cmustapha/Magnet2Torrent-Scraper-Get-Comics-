import os
import time
import requests
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://getcomics.org/page/"
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

# Fonction pour enregistrer les liens Magnet
def save_magnet_link(magnet_link):
    magnet_file_path = f"{SAVE_PATH}/magnet_links.txt"
    with open(magnet_file_path, "a", encoding="utf-8") as file:
        file.write(magnet_link + "\n")
    print(f"✅ Magnet enregistré : {magnet_link}")

# Fonction pour enregistrer les liens CBR
def save_cbr(cbr_link):
    cbr_file_path = f"{SAVE_PATH}/cbr_links.txt"
    with open(cbr_file_path, "a", encoding="utf-8") as file:
        file.write(cbr_link + "\n")
    print(f"✅ CBR enregistré : {cbr_link}")

# Récupérer la dernière page visitée
start_page = get_last_page()

# Parcourir les pages
for page in range(start_page, 1577):
    print(f"📄 Traitement de la page {page}")
    url = f"{BASE_URL}{page}/"

    try:
        # Récupérer le contenu HTML de la page
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"❌ Erreur de chargement {response.status_code} sur {url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Trouver la section contenant les articles
        section = soup.find("section", class_="page-contents post-list post-list-masonry")
        if not section:
            print("⚠ Aucune section trouvée sur cette page.")
            continue

        # Récupérer tous les articles
        articles = section.find_all("article")
        print(f"🔍 {len(articles)} articles trouvés sur cette page.")

        for article in articles:
            try:
                # Récupérer le lien de l'article
                title_element = article.find("h1", class_="post-title")
                if not title_element:
                    continue

                link = title_element.find("a")["href"]
                title = title_element.get_text(strip=True)
                print(f"📚 {title} - {link}")

                # Ouvrir la page de l'article
                article_response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
                if article_response.status_code != 200:
                    print(f"❌ Impossible d'ouvrir {link}")
                    continue

                article_soup = BeautifulSoup(article_response.text, "html.parser")

                # Chercher un lien Magnet
                magnet_link = article_soup.find("a", href=lambda href: href and "magnet:?" in href)
                if magnet_link:
                    save_magnet_link(magnet_link["href"])
                else:
                    print("⚠ Aucun lien Magnet trouvé, recherche du lien CBR...")
                    
                    # Chercher un lien CBR
                    cbr_link = article_soup.find("a", class_="aio-red", title="DOWNLOAD NOW")
                    if cbr_link:
                        save_cbr(cbr_link["href"])
                    else:
                        print("⚠ Aucun lien CBR trouvé.")

            except Exception as e:
                print(f"❌ Erreur avec un article : {e}")

        # Sauvegarde de la progression
        save_last_page(page)
        print(f"✅ Progression sauvegardée : page {page}")

        # Pause entre les requêtes pour éviter d’être bloqué par le site
        time.sleep(2)

    except Exception as e:
        print(f"❌ Erreur lors de l'accès à la page {page} : {e}")

print("🎉 Script terminé !")
