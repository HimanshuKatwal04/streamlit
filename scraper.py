# scraper.py

import requests
from bs4 import BeautifulSoup

def get_swiggy_results(query, pin):
    # Fake request (for demonstration — real scraping won't work without JavaScript rendering)
    print(f"Searching for '{query}' near pin {pin}...")

    # Simulated response (since real Swiggy pages can't be parsed without a browser)
    mock_html = """
    <html>
        <body>
            <div class="restaurant">
                <h2>Domino's Pizza</h2>
                <p>Location: Near {pin}</p>
                <p>Price: ₹299</p>
                <p>Rating: 4.3</p>
                <a href="https://www.swiggy.com/dominos">View</a>
            </div>
            <div class="restaurant">
                <h2>McDonald's Burger</h2>
                <p>Location: Near {pin}</p>
                <p>Price: ₹199</p>
                <p>Rating: 4.1</p>
                <a href="https://www.swiggy.com/mcd">View</a>
            </div>
        </body>
    </html>
    """.replace("{pin}", pin)

    soup = BeautifulSoup(mock_html, "html.parser")
    restaurants = soup.find_all("div", class_="restaurant")

    results = []
    for res in restaurants:
        name = res.find("h2").text
        location = res.find("p").text
        price = res.find_all("p")[1].text.split(":")[1].strip()
        rating = res.find_all("p")[2].text.split(":")[1].strip()
        url = res.find("a")["href"]

        results.append({
            "name": name,
            "location": location,
            "price": price,
            "rating": rating,
            "url": url
        })

    return results
