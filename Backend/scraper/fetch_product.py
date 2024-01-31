from asyncio import gather
from urllib.parse import urlparse

LORETO = "https://farmacialoreto.it"
SOCCAVO = "https://www.farmaciasoccavo.it"
EFARMA = "https://www.efarma.com"

SELECTORS = {
    LORETO: {
        "image_element": 'div.dfd-card-media img',
        "name_element": 'div.dfd-card-title',
        "price_element": "span.dfd-card-price",
        "url_element": "a.dfd-card-link"
    },
    SOCCAVO: {
        "image_element": 'div.dfd-card-media img',
        "name_element": 'div.dfd-card-title',
        "price_element": "span.dfd-card-price",
        "url_element": "a.dfd-card-link"
    },
    EFARMA: {
        "image_element": 'div.product-item-info img.product-image-photo',
        "name_element": 'div.product-item-info h2.product-item-name',
        "price_element": "div.product-item-inner span.special-price span.price",
        "url_element": "div.product-item-info a.product-item-link"
    }
}


async def get_product(product_div, url):
    # print("************ FETCHING PRODUCT ****************")
    # Query for all elements at once
    print("**** PAGE URL ", url)
    selectors = SELECTORS[url]
    image_element_future = product_div.query_selector(selectors['image_element'])
    name_element_future = product_div.query_selector(selectors['name_element'])
    price_element_future = product_div.query_selector(selectors['price_element'])
    url_element_future = product_div.query_selector(selectors['url_element'])

    # Await all queries at once
    image_element, name_element, price_element, url_element = await gather(
        image_element_future,
        name_element_future,
        price_element_future,
        url_element_future,
    )

    # Fetch all attributes and text at once
    image_url = await image_element.get_attribute('src') if image_element else None
    product_name = await name_element.inner_text() if name_element else None
    product_price = (await price_element.inner_text()).replace("€", "").replace(",", ".").strip() if price_element else None
    product_url = urlparse(await url_element.get_attribute('href')).path if url_element else None

    print({"img": image_url, "name": product_name, "price": product_price, "url": product_url})

    return {"img": image_url, "name": product_name, "price": product_price, "url": product_url}
