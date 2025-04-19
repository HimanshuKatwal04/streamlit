# scraper.py

def get_swiggy_results(query, pin):
    # Simulated food database (this would come from scraping or an API in real life)
    mock_data = [
        {
            "name": "Domino's Pizza - Veggie Paradise",
            "location": f"Domino's, Near {pin}",
            "price": "₹299",
            "rating": "4.3",
            "url": "https://www.swiggy.com/dominos",
            "description": "Contains dairy, wheat, and soy."
        },
        {
            "name": "McDonald's Chicken Burger",
            "location": f"McDonald's, Near {pin}",
            "price": "₹199",
            "rating": "4.1",
            "url": "https://www.swiggy.com/mcd",
            "description": "Contains egg, soy, and gluten."
        },
        {
            "name": "Subway Veggie Delight",
            "location": f"Subway, Near {pin}",
            "price": "₹259",
            "rating": "4.0",
            "url": "https://www.swiggy.com/subway",
            "description": "May contain traces of peanuts and gluten."
        },
        {
            "name": "Biryani Blues - Chicken Biryani",
            "location": f"Biryani Blues, Near {pin}",
            "price": "₹349",
            "rating": "4.5",
            "url": "https://www.swiggy.com/biryani-blues",
            "description": "Traditional spices, contains dairy."
        },
        {
            "name": "The Belgian Waffle Co. - Nutella Waffle",
            "location": f"Belgian Waffle, Near {pin}",
            "price": "₹180",
            "rating": "4.6",
            "url": "https://www.swiggy.com/waffle",
            "description": "Contains nuts, dairy, and eggs."
        },
        {
            "name": "Natural Ice Cream - Mango",
            "location": f"Natural Ice Cream, Near {pin}",
            "price": "₹120",
            "rating": "4.8",
            "url": "https://www.swiggy.com/natural",
            "description": "100% natural. Contains dairy only."
        },
        {
            "name": "Chai Point - Ginger Chai",
            "location": f"Chai Point, Near {pin}",
            "price": "₹80",
            "rating": "4.2",
            "url": "https://www.swiggy.com/chaipoint",
            "description": "Freshly brewed tea. Contains milk."
        },
    ]

    # Basic keyword filter for simulated search
    query_lower = query.lower()
    filtered_results = [item for item in mock_data if query_lower in item["name"].lower()]

    # Return all if no match
