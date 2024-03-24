import json
import traceback
from bs4 import BeautifulSoup
from chrome_service import ChromeService
from urllib.parse import urlparse


def handle(event, context):
    try:
        event = {
            "endpoint": "/course/top100/south-east/",
            "base_url": "https://www.golfshake.com"
        }
        site = scrape_website(event["base_url"] + event["endpoint"])
        soup = BeautifulSoup(site, features="html.parser")
        top_100 = get_top_100(soup, event["base_url"])
        return top_100

        for course in top_100:
            scraped_course = scrape_website(event["base_url"] + course)
            course_soup = BeautifulSoup(scraped_course, features="html.parser")
            course_info = extract_course_info(event["base_url"] + course, course_soup)
            print(course_info)
            exit()
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
    source = chrome.click_privacy_and_wait()
    source = chrome.get_page_source()
    return source


def get_top_100(soup, base_url):
    courses = []
    for tr in soup.find_all('tr'):
        if tr.find(class_='cardtext2'):
            course_info = {}
            course_info['name'] = tr.find_all('h2')[1].text.strip()
            course_info['url'] = base_url + tr.find('a')['href']
            parsed_url = urlparse(course_info['url'])
            path_parts = parsed_url.path.split('/')
            id_ = path_parts[3]
            slug = path_parts[4].split('.')[0].replace('_', '-').lower()
            course_info['slug'] = slug
            course_info['scrape_id'] = id_
            courses.append(course_info)
            print(sorted(course_info.items()))

    return courses