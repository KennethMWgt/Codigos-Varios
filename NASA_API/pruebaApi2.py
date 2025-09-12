import requests

# Endpoint de la NASA APOD
url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

# Usando la demo key
params = {
    "api_key": "SHMDr37hwS4DXp2FA5Zb9Nt4aaau52Tkxel0RUXL",   # cambia a tu key si tienes
    "earth_date": "2020-09-11"     # opcional, formato YYYY-MM-DD
}
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    photos = data.get("photos",[])
    for photo in photos: 
        print("ID:", photo["id"])
        print("Camera:", photo["camera"]["name"])
        print("Image:", photo["img_src"])
        print("Earth Date:", photo["earth_date"])
        print("Rover:", photo["rover"]["name"])
        print("-" * 120)
else:
    print("Error:", response.status_code, response.text)