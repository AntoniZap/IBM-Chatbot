# NOTICE: This idea was started in the earlier stages of development
# It is no longer being worked on.
# It has been uploaded for proof of work, and to adapt if a site is found that allows scraping

'''
import requests
from bs4 import BeautifulSoup
import pandas
import numpy

url = "exampleurl.com"
response = requests.get(url, headers=custom headers)
soup = BeautifulSoup(response.text, "lxml")
reviews = np.array([])

title_element = soup.select_one('#productTitle')
title = title_element.text.strip()

price_element = soup.select_one('span.a-price').select_one('span.a-offscreen')
price = price_element.text

reviews_elements = soup.select("div.review")

for review in reviews_elements:
    rating_element = review.select_one("i.review-rating")
    rating = rating_element.text if r_rating_element else None

    review_content_element = review.select_one("span.review-text")
    review_content = review_content_element.text if review_content_element else None

    date_element= review.select_one("span.review-date")
    date = review_date_element.text if date_element else None

    review = {"rating": rating,
              "content": review_content
              "date": date}
    
    reviews = np.append(reviews, review)

'''

# src: https://www.youtube.com/watch?v=w3XcMfyUGxY
