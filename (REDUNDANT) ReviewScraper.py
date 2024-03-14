# Note - Idea no longer being worked on
# Uploaded for proof of work, and to adapt if a site is found that allows scraping

import requests
from bs4 import BeautifulSoup
import pandas

url = ""
response = requests.get(url, headers=custom headers)
soup = BeautifulSoup(response.text, "lxml")
reviews = []

title_element = soup.select_one('#productTitle')
title = title_element.text.strip()

price_element = soup.select_one('span.a-price').select_one('span.a-offscreen')
price = price_element.text

reviews_elements = soup.select("div.review")

for review in reviews_elements:
    review_rating_element = review.select_one("i.review-rating")
    review_rating = review_rating_element.text

    review_content_element = review.select_one("span.review-text")
    review_content = review_content_element.text

    review = {"rating": review_rating,
              "content": review_content}
    
    reviews.append(review)

#src: https://www.youtube.com/watch?v=w3XcMfyUGxY