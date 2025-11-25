"""
Debug script to see what URLs we're requesting
"""
import requests

base_url = "https://www.therapie.de/therapeutensuche/ergebnisse/"
zip_code = "10117"

# Page 1
params_page1 = {
    "ort": zip_code,
    "abrechnungsverfahren": 1,
    "terminzeitraum": 4,
}

# Page 2
params_page2 = {
    "ort": zip_code,
    "abrechnungsverfahren": 1,
    "terminzeitraum": 4,
    "seite": 2
}

# Build the actual URLs that will be requested
req1 = requests.Request('GET', base_url, params=params_page1)
prepared1 = req1.prepare()

req2 = requests.Request('GET', base_url, params=params_page2)
prepared2 = req2.prepare()

print("URL for page 1:")
print(prepared1.url)
print()
print("URL for page 2:")
print(prepared2.url)
