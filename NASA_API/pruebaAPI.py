import requests

# Endpoint de la NASA APOD
url = "https://api.nasa.gov/planetary/apod"

# Usando la demo key
params = {
    "api_key": "SHMDr37hwS4DXp2FA5Zb9Nt4aaau52Tkxel0RUXL",   # cambia a tu key si tienes
    "date": "2025-09-09"     # opcional, formato YYYY-MM-DD
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Title:", data["title"])
    print("Date:", data["date"])
    print("Explanation:", data["explanation"])
    print("Image URL:", data["url"])
else:
    print("Error:", response.status_code, response.text)