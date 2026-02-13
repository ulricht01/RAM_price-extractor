from load import *
from db import *
from bs4 import BeautifulSoup
import datetime
from analysis import *
import fake_useragent
from curl_cffi import requests

ramky = Database("ramky")

if __name__ == "__main__":
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    try:
        r = requests.get(
            url, 
            headers=headers, 
            impersonate="chrome120", 
            allow_redirects=True
        )
        r.raise_for_status() 
    except Exception as e:
        print(f"Chyba při stahování stránky: {e}")
        exit()
    
    soup = BeautifulSoup(r.text, "html.parser")
    container = soup.find("div", class_ = "browsingitemcontainer")
    items = container.find_all("div", class_="browsingitem")

    if(not ramky.check_for_today_data(date)):
        for item in items:
            name = item.find("a", class_ ="name").text
            price_tag = item.find("span", class_="price-box__primary-price")

            if name and price_tag:
                price = "".join(filter(str.isdigit, price_tag.text))

                try:
                    price = int(price)
                    ramky.insert_data(name, price, date)
                except ValueError:
                    print(f"Přeskakuji {name} - nepodařilo se získat cenu.")

        vsechna_data = ramky.export_data()
        process_and_save_report(vsechna_data)
        
        ramky.commit_and_close()

    else:
        raise Exception("Dnes už byla data extrahována!")

