# Aliasy:
- checkdb -> Spustí skript manuálně
- update-ram -> aktualizuje soubory pomocí git fetch a vytvoří nový docker image 

# PM2 (Pro běh API na pozadí)
- pm2 list –> Ukáže tabulku se všemi běžícími procesy, kolik žerou paměti a kolikrát spadly.
- pm2 logs –> Zobrazí v reálném čase výpisy z console.log (velmi důležité pro ladění).
- pm2 stop moje-aplikace –> Zastaví proces.
- pm2 restart moje-aplikace –> Restartuje ho (např. po úpravě kódu).
- pm2 monit –> Otevře interaktivní dashboard přímo v terminálu.
-pm2 delete moje-aplikace -> odstraní proces