from bs4 import BeautifulSoup

def parse_listing_page(html):
    soup = BeautifulSoup(html, "html.parser")
    listings = []
    items = soup.select(".zu-itemmod")
    for item in items:
        title = item.select_one(".zu-info h3 a")
        price = item.select_one(".zu-side .price")
        detail = item.select_one(".details-item")
        position = item.select_one(".zu-info .details-item")

        listings.append({
            "title": title.text.strip() if title else None,
            "price": price.text.strip() if price else None,
            "detail": detail.text.strip() if detail else None,
            "position": position.text.strip() if position else None,
        })
    return listings