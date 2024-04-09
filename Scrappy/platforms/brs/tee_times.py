import json
import traceback
from bs4 import BeautifulSoup
from chrome_service import ChromeService
import pendulum

def handle(event):
    try:
        url = event.get("url")
        date_obj = pendulum.from_format(event.get('date'), 'YYYY-MM-DD')
        # if date_obj > pendulum.now().add(weeks=2):
        #     return {
        #         "statusCode": 400,
        #         "body": json.dumps({"message": "Date is too far in the future."})
        #     }
        content = scrape_website(url, date_obj)
        soup = BeautifulSoup(content, features="html.parser")
        tee_times = get_tee_times(soup, url)
        return {
            "statusCode": 200,
            "body": json.dumps(tee_times)
        }
    except Exception as e:
        error_message = "An error occurred while handling BRSz platform request."
        print(error_message)
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps({"message": error_message})
        }


def scrape_website(url, date):
    chrome = ChromeService()
    chrome.get_url(url)
    chrome.click_by_id('desktop-teesheet-filter-datepicker')
    chrome.wait()
    chrome.screenshot("date_picker")
    if (chrome.is_text_visible(date.format('MMMM YYYY'))) is False:
        chrome.click_by_xpath('//html/body/div[4]/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div[3]/svg')
        chrome.wait()
    chrome.click_by_class_where_content('c-day-content', date.format('D'))
    chrome.screenshot("selected_day")
    chrome.wait()
    chrome.wait_till_gone_by_class('.popover-origin.direction-bottom.align-left')
    chrome.wait()
    chrome.screenshot("loaded")
    chrome.wait_by_class('column.is-one-third-mobile.is-one-quarter-tablet.is-one-fifth-desktop')
    source = chrome.get_loaded_source()
    chrome.close()
    return source


def get_tee_times(content, url):
    tee_times = []
    tee_times_panel = content.find('div', class_='teetimes-panel')
    for available_tees in tee_times_panel.find_all('div', class_='column'):
        tee_time = available_tees.find('div', class_='is-teetime').text
        print(tee_time)

        # one_ball_price = available_tees.find('div', class_='one-ball').text
        # two_ball_price = available_tees.find('div', class_='two-balls').text
        # three_ball_price = available_tees.find('div', class_='three-balls').text
        # four_ball_price = available_tees.find('div', class_='four-balls').text

        # tee_times.append({
        #     "time": tee_time.split(" ")[1],
        #     "date": tee_time.split(" ")[0],
        #     "bookingUrl": url,
        #     "cost_per_ball": {
        #         "one_ball": one_ball_price,
        #         "two_balls": two_ball_price,
        #         "three_balls": three_ball_price,
        #         "four_balls": four_ball_price
        #     }
        # })

    return tee_times
