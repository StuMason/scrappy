import json
import pytest
from bs4 import BeautifulSoup


def test_soup_get_tee_times():
    with(open("./tests/_fixtures/wanstead_source.html", "r")) as f:
        wanstead_source = f.read()
        soup = BeautifulSoup(wanstead_source, features="html.parser")
        tee_times = []
        for time in soup.find_all('div', class_="tee available"):
            prices = time.find_all("div", class_="price")
            tee_prices = []
            for price in prices:
                ball_number = price['class'][1].split('-')[-1]
                value = price.find_all("div", class_="value")
                tee_price = {
                    "balls": ball_number,
                    "cost": value[0].get_text(),
                }
                tee_prices.append(tee_price)
            tee_time_data = {
                "time": time["data-teetime"],
                "prices": tee_prices,
            }
            tee_times.append(tee_time_data)
        print(tee_times)



    