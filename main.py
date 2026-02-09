from load import *
from db import *
from bs4 import BeautifulSoup
import datetime
from analysis import *
from playwright.sync_api import sync_playwright

ramky = Database("ramky")

def get_html_with_playwright(url):
    with sync_playwright() as p:
        # Spustíme prohlížeč (headless=True je pro GitHub Actions nutnost)
        browser = p.chromium.launch(headless=True)
        # Nastavení uživatelského agenta, aby to vypadalo jako reálný člověk
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        page = context.new_page()
        
        # Přejdeme na stránku a počkáme, až se načte síťový provoz
        page.goto(url, wait_until="networkidle")
        
        # Získáme obsah HTML
        html = page.content()
        browser.close()
        return html

if __name__ == "__main__":
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    try:
        print("Spouštím prohlížeč přes Playwright...")
        html_content = get_html_with_playwright(url)
        soup = BeautifulSoup(html_content, "html.parser")
        
        container = soup.find("div", class_="browsingitemcontainer")
        
        if container is None:
            print("Kritická chyba: Kontejner nebyl nalezen ani přes Playwright.")
            # Zde můžeme vypsat kousek pro kontrolu, jestli tam není Captcha
            exit()

        items = container.find_all("div", class_="browsingitem")

        if not ramky.check_for_today_data(date):
            for item in items:
                name_tag = item.find("a", class_="name")
                price_tag = item.find("span", class_="price-box__primary-price")

                if name_tag and price_tag:
                    name = name_tag.text.strip()
                    price = "".join(filter(str.isdigit, price_tag.text))
                    try:
                        price = int(price)
                        ramky.insert_data(name, price, date)
                    except ValueError:
                        print(f"Přeskakuji {name} - nepodařilo se získat cenu.")

            ramky.conn.commit()
            print("Data byla úspěšně stažena.")
            
            vsechna_data = ramky.export_data()
            process_and_save_report(vsechna_data)
        else:
            print("Dnes už byla data extrahována!")
            
    finally:
        ramky.commit_and_close()