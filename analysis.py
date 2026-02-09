import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import datetime

def process_and_save_report(raw_data):
    """Zpracuje data a pokud je pondělí, uloží graf jako PNG."""
    
    # 1. Příprava dat
    df = pd.DataFrame(raw_data, columns=["name", "price", "date"])
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])

    avg_df = df.groupby("date")["price"].mean().reset_index()
    avg_df.columns = ["date", "avg_price"]
    avg_df = avg_df.sort_values(by="date")

    # Klouzavý průměr
    avg_df["moving_avg"] = avg_df["avg_price"].rolling(window=7, min_periods=1).mean()

    # 2. Kontrola dne v týdnu (0 = Pondělí)
    now = datetime.datetime.now()
    if now.weekday() == 0:
        print("Je pondělí, generuji a ukládám týdenní report...")
        
        plt.figure(figsize=(10, 6))
        
        # Vykreslení
        plot = seaborn.lineplot(
            data=avg_df, 
            x="date", 
            y="avg_price", 
            marker="o", 
            markersize=8, 
            label="Denní průměr"
        )
        seaborn.lineplot(
            data=avg_df, 
            x="date", 
            y="moving_avg", 
            linestyle="--", 
            color="red", 
            label="7denní trend"
        )

        # Formátování osy X
        plt.xticks(avg_df["date"], rotation=45)
        plot.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d.%m.%Y'))

        # Odstranění popisků a nastavení titulu
        plt.xlabel("")
        plt.ylabel("")
        plt.legend(loc="upper left")
        plt.title("Report průměrných cen RAM (24 nejlevnějších dle Alzy)")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # ULOŽENÍ MÍSTO ZOBRAZENÍ
        filename = f"report_cen_{now.strftime('%Y_%m_%d')}.png"
        plt.savefig(filename)
        plt.close()  # Zavře graf, aby nezůstal v paměti
        print(f"Graf byl uložen jako {filename}")
    else:
        print(f"Dnes je {now.strftime('%A')}, report se generuje pouze v pondělí.")