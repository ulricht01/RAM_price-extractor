-- Smazání starého formátu (pokud bys tam ještě měl tečky)
-- UPDATE ramky SET dt_insert = substr(dt_insert, 7, 4) || '-' || substr(dt_insert, 4, 2) || '-' || substr(dt_insert, 1, 2) WHERE dt_insert LIKE '%.%.%';

SELECT 
    dt_insert, 
    Round(avg(price), 2) AS prumerna_ram 
FROM ramky 
GROUP BY 1
ORDER BY dt_insert ASC;