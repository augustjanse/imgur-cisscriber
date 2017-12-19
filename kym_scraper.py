from lxml import html
import requests

for i in range(1,105):
    page = requests.get('http://knowyourmeme.com/search?page=' + str(i) + '&q=status%3Aconfirmed+category%3Ameme&sort=newest')
    tree = html.fromstring(page.content)

    for element in tree.cssselect("td > h2 > a"):
        memes = element.text_content().split(" / ")
        if len(memes) > 1:
            print(memes)


