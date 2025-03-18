# Magnet2Torrent-Scraper-Get-Comics

Ce projet permet de **scraper** des liens **Magnet** depuis [GetComics](https://getcomics.org/) en utilisant **Selenium**, puis de **convertir ces liens en fichiers `.torrent`** grâce à `aria2c`.

---

## 🚀 Fonctionnalités

✅ Scrape automatiquement les **articles Marvel Now**  
✅ Extrait les **liens Magnet** des articles  
✅ Convertit les Magnet en **fichiers `.torrent`**  
✅ Stocke les fichiers `.torrent` dans un dossier  
✅ Utilise `aria2c` pour la conversion

---

## 📌 Prérequis

- Python

```bash
git clone https://github.com/AdamchDarkness/Magnet2Torrent-Scraper-Get-Comics-.git
cd magnet2torrent-scraper
pip install selenium
pip install webdriver-manager
```

## 🚀 Utilisation

Exécutez le script principal :

```bash
python main.py
python mainDC.py
```

#Le programme va :

- Scraper les articles de GetComics.
- Extraire les liens Magnet.
- Les convertir en .torrent avec aria2c.
- Stocker les .torrent dans torrents/.
