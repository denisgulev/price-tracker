import asyncio
from playwright.async_api import async_playwright
import json
import os
from fetch_product import get_product
from requests import post
from concurrent.futures import ProcessPoolExecutor
import sys

AMAZON = "https://amazon.it"
LORETO = "https://farmacialoreto.it"
SOCCAVO = "https://www.farmaciasoccavo.it"
EFARMA = "https://www.efarma.com"

URLS = {
    LORETO: {
        "search_field_query": 'input[name="search"]',
        "search_button_query": 'button[type="button"]',
        "product_selector": "div.dfd-card",
        "search_result": "div.dfd-results"
    },
    SOCCAVO: {
        "search_field_query": 'input#search',
        "search_button_query": '#search_mini_form > button:nth-child(2)',
        "product_selector": "div.dfd-card",
        "search_result": "div.dfd-results"
    },
    EFARMA: {
        "search_field_query": 'input#search',
        "search_button_query": '#search_mini_form > button:nth-child(2)',
        "product_selector": "li.product-item",
        "search_result": "div.products-list"
    }
}

available_urls = URLS.keys()


# def load_auth():
#     FILE = os.path.join("scraper", "auth.json")
#     with open(FILE, "r") as f:
#         return json.load(f)

# # place your bright-data credentials in auth.json file with keys: "username", "password" and "host"
# cred = load_auth()
# auth = f'{cred["username"]}:{cred["password"]}'
# browser_url = f'https://farmacialoreto.it'


async def search(metadata, page, search_text):
    print(f"Searching for {search_text} on {page.url}")
    search_field_query = metadata.get("search_field_query")
    search_button_query = metadata.get("search_button_query")
    search_result = metadata.get("search_result")

    if search_field_query and search_button_query:
        # print("Filling input field")
        search_box = await page.wait_for_selector(search_field_query)
        await search_box.type(search_text)
        await page.keyboard.press("Enter")
        # print("Pressing search button")
        # print(f'Waiting for ${search_button_query} to be visible')
        # button = await page.wait_for_selector(search_button_query)
        # await button.click()
        # print("Waiting for search results")
        await page.wait_for_selector(search_result)
    else:
        raise Exception("Could not search.")

    await page.wait_for_load_state()
    return page


async def get_products(page, search_text, selector, get_product, url):
    # print("Retreiving products.")
    product_divs = await page.query_selector_all(selector)
    valid_products = []
    words = search_text.split(" ")
    background_tasks = set()
    # print(product_divs)

    async def extract_info(p_div):
        product = await get_product(p_div, url)

        if not product["price"] or not product["url"]:
            return

        for word in words:
            if not product["name"] or word.lower() not in product["name"].lower():
                break
        else:
            valid_products.append(product)

    # async with asyncio.TaskGroup() as tg: --> TaskGroup is available from python3.11
    for div in product_divs:
        task = asyncio.create_task(extract_info(div))
        await task
        # Add task to the set. This creates a strong reference.
        background_tasks.add(task)
        # To prevent keeping references to finished tasks forever,
        # make each task remove its own reference from the set after
        # completion:
        task.add_done_callback(background_tasks.discard)
        # tg.create_task(task(div))

    # print("************ valid_products *************")                print(valid_products)

    # print(valid_products)
    return valid_products

# TODO - see where can this be used
# def save_results(results):
#     data = {"results": results}
#     FILE = os.path.join("Scraper", "results.json")
#     with open(FILE, "w") as f:
#         json.dump(data, f)


def post_results(results, endpoint, search_text, source):
    headers = {
        "Content-Type": "application/json"
    }
    data = {"data": results, "search_text": search_text, "source": source}

    response = post("http://localhost:5000" + endpoint,
                    headers=headers, json=data)

# executes scraper in a browser window
# retrieve products
# posts results on '/results' route
async def main(url, search_text, response_route):
    metadata = URLS.get(url)
    
    if not metadata:
        print("Invalid URL.")
        return

    print("post metadata check")
    async with async_playwright() as pw:
        print("Connecting to browser.")
        browser = await pw.chromium.launch() #(headless=False)
        page = await browser.new_page()
        print(f"Connected to ${url}." )
        await page.goto(url, timeout=3000000)
        print("Page loaded.")
        await page.wait_for_selector("#search")
        print("Loaded initial page.")
        search_page = await search(metadata, page, search_text)

        def func(x): return None
        if URLS[url]:
            func = get_product
        else:
            raise Exception("Invalid URL")

        results = await get_products(search_page, search_text, metadata["product_selector"], func, url)
        print("Saving results.")
        print(results)
        post_results(results, response_route, search_text, url)

        await browser.close()

if __name__ == "__main__":
    # test script
    asyncio.run(main(SOCCAVO, "mgk vis"))
