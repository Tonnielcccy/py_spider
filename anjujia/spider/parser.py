from bs4 import BeautifulSoup


def parse_listing_page(html):
    soup = BeautifulSoup(html, "html.parser")
    listings = []
    items = soup.select(".zu-itemmod")  # 每个房源卡片

    for item in items:
        # 标题
        title_tag = item.select_one(".zu-info h3 a b.strongbox")
        title = title_tag.text.strip() if title_tag else None

        # 价格
        price_tag = item.select_one(".zu-side .price")
        unit_tag = item.select_one(".zu-side .unit")
        price = price_tag.text.strip() if price_tag else None
        unit = unit_tag.text.strip() if unit_tag else None

        # 户型信息（如“2室1厅 | 40平米 | 高层(共17层)”）
        detail_tag = item.select_one("p.details-item.tag")
        layout, area, floor = (None, None, None)
        if detail_tag:
            parts = detail_tag.text.strip().split("|")
            if len(parts) == 3:
                layout = parts[0].strip()
                area = parts[1].strip()
                floor = parts[2].strip()

        # 小区名（地址的 <a> 标签部分）
        community_tag = item.select_one("address.details-item.tag a")
        community = community_tag.text.strip() if community_tag else None

        # 位置（address 中除了小区名的部分）
        address_tag = item.select_one("address.details-item.tag")
        location = address_tag.text.replace(community, "").strip() if community and address_tag else None

        # 标签（如“邻地铁”、“押一付一”等）
        tag_items = item.select("p.bot-tag span.cls-common")
        tags = [tag.text.strip() for tag in tag_items] if tag_items else []

        listings.append({
            "title": title,
            "price": price,
            "unit": unit,
            "layout": layout,
            "area": area,
            "floor": floor,
            "community": community,
            "location": location,
            "tags": tags
        })

    return listings
