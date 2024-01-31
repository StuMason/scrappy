import json
import traceback
from bs4 import BeautifulSoup
from chrome_service import ChromeService


def handle(event, context):
    try:
        endpoint = event["endpoint"]
        content = scrape_website(endpoint)
        soup = BeautifulSoup(content, features="html.parser")
        links = get_links(soup, endpoint)
        # reduce links array to 10
        links = links[:10]
        for link in links:
            article = scrape_website(link["href"])
            soup = BeautifulSoup(article, features="html.parser")
            article = soup.find("article")
            if article:
                link["article"] = article.get_text()

        return links

        # return {
        #     "statusCode": 200,
        #     "body": json.dumps({"data": content}),
        # }
    except Exception:
        error_message = "An error occurred while processing the request."
        print(error_message)
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps({"error": error_message})
        }


def scrape_website(endpoint):
    chrome = ChromeService()
    chrome.get_url(endpoint)
    source = chrome.get_loaded_source()
    chrome.close()
    return source


def get_links(content, endpoint):
    links = []

    for link in content.find_all('a', href=True):
        text = link.get_text()
        href = link['href']

        if len(text.split()) < 4:
            continue

        skip = ["Audio", "Video", "our", "BBC"]
        if any(word in text for word in skip):
            continue

        if not href.startswith(endpoint):
            href = endpoint + href

        links.append({
            "text": text,
            "href": href
        })

    return links
