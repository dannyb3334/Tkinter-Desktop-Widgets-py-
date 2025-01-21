import requests as r
from bs4 import BeautifulSoup as bs
from PIL import Image
from io import BytesIO 
import json
#Get Webpage
def update_article():
    try:
        response_page = r.get("https://en.wikipedia.org/wiki/Main_Page")
        #Take Html to txt
        wiki_html_text = response_page.text
        soup = bs(wiki_html_text, 'html.parser')
        #Find Image and Article
        article_text_new = (soup.find_all("p"))[0].text[:-19] + "..(Click to read more!)"
        article_image = ((soup.find_all("img"))[3])['src']
        #Read Record Of Current Article
        with open("app/resources/ArticleText.json", "r") as jsonFile:
            article_saved = json.load(jsonFile)
        #Replace Record If New Article Found
        if article_saved != article_text_new:
            with open("app/resources/ArticleText.json", "w") as jsonFile:
                json.dump(article_text_new, jsonFile)
                response_image = r.get("http:" + article_image)
                img = Image.open(BytesIO(response_image.content))
                img = img.save("app/resources/ArticleImage.png")
            print("***Current article copy updated!***")
        #Otherwise Keep Saved Article
        else:
            print("***Article is a saved copy***")
    except:
        print("***Unable to fetch webpage...Please check internet connection\nArticle is a saved copy***")

if __name__ == "__main__":
    update_article()