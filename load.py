from fake_useragent import UserAgent

url = "https://www.alza.cz/levne-pameti-ddr4-32-gb-pro-pc/18858913.htm"

ua = UserAgent(platforms="pc")

headers = {
    'User-Agent': ua.chrome,
    'Accept-Language': 'cs-CZ,cs;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}