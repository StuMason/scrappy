import json
import traceback
from bs4 import BeautifulSoup
from chrome_service import ChromeService
import pendulum

def handle(event):
    try:
        url = event.get("url")
        date_obj = pendulum.from_format(event.get('date'), 'YYYY-MM-DD')
        print(date_obj)
        date = date_obj.format('dddd Do MMMM')
        print(date)
        exit()

        content = scrape_website(url)

        soup = BeautifulSoup(content, features="html.parser")

        tee_times = get_tee_times(soup, url)
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


def scrape_website(url):
    chrome = ChromeService()
    chrome.get_url(url)
    chrome.wait()
    source = chrome.get_loaded_source()
    chrome.close()
    return source


def get_tee_times(content, url):
    tee_times = []
    for available_tees in content.find_all('div', class_='tee available'):

        tee_times.append({
            "time": tee_time.split(" ")[1],
            "date": tee_time.split(" ")[0],
            "bookingUrl": url,
            "cost_per_ball": cost_per_ball
        })

    return tee_times
