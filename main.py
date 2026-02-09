from load import *
from db import *
from bs4 import BeautifulSoup
import datetime
from analysis import *
from playwright.sync_api import sync_playwright

ramky = Database("ramky")

def get_html_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Použijeme reálnější rozlišení a maskování
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # 1. Nastavíme delší timeout pro celou akci (60s)
        page.set_default_timeout(60000)
        
        # 2. Čekáme jen na DOMContentLoaded (rychlejší a stabilnější)
        print(f"Otevírám URL: {url}")
        page.goto(url, wait_until="domcontentloaded")
        
        # 3. Krátce počkáme (např. 2 sekundy), aby se stačily vykreslit ceny
        page.wait_for_timeout(2000)
        
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