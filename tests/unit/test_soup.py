import json
import pytest
from bs4 import BeautifulSoup, Comment


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



def test_soup_get_course_text():
    with(open("./tests/_fixtures/goldshake_course.html", "r")) as f:
        wanstead_source = f.read()
        soup = BeautifulSoup(wanstead_source, features="html.parser")

        # Remove the div with id 'golfshakehead'
        golfshakehead_div = soup.find('div', id='golfshakehead')
        if golfshakehead_div:
            golfshakehead_div.extract()

        # Remove all elements with class 'review-block'
        review_blocks = soup.find_all(class_='review-block')
        for review_block in review_blocks:
            review_block.extract()

        # Find the element with name 'postreview' and remove everything after it
        postreview_element = soup.find('a', {'name': 'postreview'})
        if postreview_element:
            # Get the parent of the 'postreview' element
            parent = postreview_element.parent
            # Find all siblings after 'postreview' element and remove them
            for sibling in parent.find_next_siblings():
                sibling.extract()

        # Remove all <script> tags
        for script in soup.find_all('script'):
            script.decompose()

        # Remove all comments
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        # content = soup.get_text().replace('\n', '')
        print(soup)