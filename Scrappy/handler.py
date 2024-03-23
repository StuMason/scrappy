import json
import traceback
from bs4 import BeautifulSoup
from chrome_service import ChromeService


def handle(event, context):
    try:
        endpoint = event["endpoint"]
        content = scrape_website(endpoint)
        # save content to a file
        print(content)
        exit()
        soup = BeautifulSoup(content, features="html.parser")
        links = get_tee_times(soup, endpoint)
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


def get_tee_times(content, endpoint):
    tee_times = []

    for time in content.find_all('div', content.find_all("div", class_="tee available")):
        print(time)
        exit()
        text = time.get_text()
        href = time['href']

        if len(text.split()) < 4:
            continue

        skip = ["Audio", "Video", "our", "BBC"]
        if any(word in text for word in skip):
            continue

        if not href.startswith(endpoint):
            href = endpoint + href

        tee_times.append({
            "text": text,
            "href": href
        })

    return tee_times
