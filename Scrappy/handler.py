import json
import traceback
from bs4 import BeautifulSoup, Comment
from chrome_service import ChromeService
from urllib.parse import urlparse, parse_qs


def handle(event, context):
    try:
        event = {
            "endpoint": "/course/top100/south-east/",
            "base_url": "https://www.golfshake.com",
            "course_url": "https://www.golfshake.com/course/view/16624/Westerham_Golf_Club.html",
        }
        # if "course_url" in event:
        #     scraped_course = scrape_website(event["course_url"])
        #     course_soup = BeautifulSoup(scraped_course, features="html.parser")
        #     course = {
        #         "name": "Westerham Golf Club",
        #         "scrape_id": "16624",
        #         "slug": "westerham-golf-club",
        #         "url": "https://www.golfshake.com/course/view/16624/Westerham_Golf_Club.html"
        #     }
        #     course_info = extract_course_info(course_soup, course)
        #     return course_info

        site = scrape_website(event["base_url"] + event["endpoint"])
        soup = BeautifulSoup(site, features="html.parser")
        top_100 = get_top_100(soup, event["base_url"])
        courses = []
        for course in top_100:
            """
            ('name', 'Westerham Golf Club')
            ('scrape_id', '16624')
            ('slug', 'westerham-golf-club')
            ('url', 'https://www.golfshake.com/course/view/16624/Westerham_Golf_Club.html')
            """
            scraped_course = scrape_website(course["url"])
            course_soup = BeautifulSoup(scraped_course, features="html.parser")
            course_info = extract_course_info(course_soup, course)
            staging_data = {
                'scrape_url': course["url"],
                'scrape_id': course_info["scrape_id"],
                'scrape_content': course_info,
                'processed': False
            }
            courses.append(staging_data)
        return json.dumps(courses)
    except Exception:
        error_message = "An error occurred while processing the request."
        print(error_message)
        print(traceback.format_exc())
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}


def scrape_website(endpoint):
    chrome = ChromeService()
    chrome.get_url(endpoint)
    source = chrome.get_loaded_source()
    source = chrome.click_privacy_and_wait()
    source = chrome.get_page_source()
    return source


def get_top_100(soup, base_url):
    courses = []
    for tr in soup.find_all("tr"):
        if tr.find(class_="cardtext2"):
            course_info = {}
            course_info["name"] = tr.find_all("h2")[1].text.strip()
            course_info["url"] = base_url + tr.find("a")["href"]
            parsed_url = urlparse(course_info["url"])
            path_parts = parsed_url.path.split("/")
            id_ = path_parts[3]
            slug = path_parts[4].split(".")[0].replace("_", "-").lower()
            course_info["slug"] = slug
            course_info["scrape_id"] = id_
            courses.append(course_info)
            """
            ('name', 'Westerham Golf Club')
            ('scrape_id', '16624')
            ('slug', 'westerham-golf-club')
            ('url', 'https://www.golfshake.com/course/view/16624/Westerham_Golf_Club.html')
            """
    return courses


def extract_course_info(soup, course_info):
    try:
        address = soup.find("div", itemprop="address")
        if address:
            link = address.find("a")
            if link and "lat" in link["href"] and "lon" in link["href"]:
                lat = link["href"].split("lat=")[1].split("&")[0]
                lon = link["href"].split("lon=")[1].split("&")[0]

        # Extract business information
        business_div = soup.find("div", itemtype="http://schema.org/LocalBusiness")
        if business_div:
            image_div = soup.find("div", id="section_content_640")
            if image_div:
                img_tag = image_div.find("img")
                if img_tag:
                    image = img_tag["src"]
                else:
                    image = None
            info = business_div.find(itemprop="description").text.strip()

        overview = soup.find("div", id="overview")

        ameneites = overview.find_all("div", class_="card25review cardcolumns")
        list_of_amenities = []
        for amenity in ameneites:
            list_of_amenities.append(amenity.text.strip())

        for tag in soup.select(
            "#golfshakehead, .review-block, .footer_placeholder"
        ):
            tag.decompose()

        remove_ads = soup.find_all("div", {"id": "section_content_970", "class": "nowrap"})
        for div in remove_ads[-3:]:
            div.decompose()

        content_text = (
            soup.get_text()
            .strip()
            .replace("\n", " ")
            .replace("\r", " ")
        )

        course = {
            "scrape_id": course_info["scrape_id"],
            "scrape_url": course_info["url"],
            "lat": lat,
            "lon": lon,
            "facilities": list_of_amenities,
            "name": course_info["name"],
            "slug": course_info["slug"],
            "address": address.text.strip(),
            "image": image,
            "info": info,
            "raw_content": content_text,
        }

        return course
    except Exception:
        traceback.print_exc()
        course = {
            "scrape_id": course_info["scrape_id"],
            "scrape_url": course_info["url"],
            "name": course_info["name"],
            "slug": course_info["slug"],
        }
        return course
