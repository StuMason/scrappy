import json
import traceback
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urlencode
from chrome_service import ChromeService

def handle(event):
    try:
        url = event.get("url")
        date = event.get("date")
        parsed_url = urlparse(url)
        root_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
        query_params = {'date': date}
        endpoint = root_url + parsed_url.path + "?" + urlencode(query_params)
        content = scrape_website(endpoint)
        soup = BeautifulSoup(content, features="html.parser")
        print("Getting Tee Times for " + date + " from " + url + " ...")
        tee_times = get_tee_times(soup, root_url)
        return {
            "statusCode": 200,
            "body": json.dumps(tee_times)
        }
    except Exception as e:
        error_message = "An error occurred while handling clubv1 platform request."
        print(error_message)
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps({"message": error_message})
        }

def scrape_website(endpoint):
    chrome = ChromeService()
    chrome.get_url(endpoint)
    source = chrome.get_loaded_source()
    chrome.close()
    return source


def get_tee_times(content, root_url):
    tee_times = []
    for available_tees in content.find_all('div', class_='tee available'):
        tee_time = available_tees.get('data-teetime')
        cost_per_ball = None
        ball_1_div = available_tees.find('div', class_='price ball-1')
        if ball_1_div:
            value_div = ball_1_div.find('div', class_='value')
            if value_div:
                cost_per_ball = value_div.text.strip()
                if cost_per_ball == 0:
                    continue

        tee_times.append({
            "time": tee_time.split(" ")[1],
            "date": tee_time.split(" ")[0],
            "bookingUrl": root_url + available_tees.find("a")["href"],
            "cost_per_ball": cost_per_ball
        })

    return tee_times
