import nltk
from newspaper import Article
import requests
import bs4
from datetime import date
import pandas as pd

def extract_html_content(target_url):
    response = requests.get(target_url)
    return response.text

topic = input("Topic: ")
pages = int(input("How many pages do you want to scrape (1-10): "))

nltk.download('punkt')

X = ['Date', 'Title', 'About', 'Key Points', 'Whole Text', 'URL']

df = pd.DataFrame(columns=X)

for i in range(1,pages+1):
    url = 'https://www.economist.com/search?q=' + ("+".join(topic.split(" "))) + "&page=" + str(i)
    html_content = extract_html_content(url)
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    aTags = soup.find_all("a", class_="_search-result")
    links = []
    for i in aTags:
        links.append(i.get('href'))
    for link in links:
        article = Article(link)
        article.download()
        article.parse()
        article.nlp()
        if "audio" in article.text.split("\n\n")[1]:
            continue
        try:
            print("\nDate:", article.publish_date.date(), "\nTitle:", article.title, "\nAbout:", article.text.split("\n\n")[1], "\n")
            df.loc[len(df)] = [article.publish_date.date(), article.title, article.text.split("\n\n")[1], article.summary, article.text, link]
        except:
            continue     

df.to_csv("Processed Topics\{}.csv".format(topic))

input("DONE!")