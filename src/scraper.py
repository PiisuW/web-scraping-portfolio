import requests
from bs4 import BeautifulSoup
import json
import time


BASE_URL = "https://books.toscrape.com/catalogue/"
current_page = 1
all_books = []

while True:
    try:

        page_url = f"{BASE_URL}page-{current_page}.html"
        print(f"Scrapping page {current_page}: {page_url}")

        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        items_elements = soup.find_all("article", class_="product_pod")

        if not items_elements:
            print(f"Aucun livre trouvé sur la page {current_page}. Fin du scraping")
            break


        for item in items_elements:


            title = item.find("h3").a["title"]
            
            price = item.find("p", class_="price_color").text.strip()

            star = item.find("p", class_="star-rating")["class"][1] + " stars"

            availability = item.find("p", class_="instock availability").text.strip()

            print(f"{title} | {price} | {star} | {availability}")

            all_books.append({
                "title": title,
                "price": price,
                "rating": star,
                "availability" : availability
            })

        next_button = soup.select_one("li.next > a")

        if not next_button:
            print("Dernière page atteinte.")
            break

        current_page += 1
        time.sleep(1)

    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP sur la page {current_page}: {e}")
        break
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        break

# Export en JSON
with open("books.json", "w", encoding="utf-8") as f:
    json.dump(all_books, f, ensure_ascii=False, indent=4)

print("\nExport terminé : books.json créé avec succès!")