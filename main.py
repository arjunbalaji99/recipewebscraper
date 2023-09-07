import re
import requests
from bs4 import BeautifulSoup

recipe_url = 'https://www.allrecipes.com/recipe/6849/boiled-bagels/'
# recipe_url = 'https://www.allrecipes.com/recipe/15431/beef-and-vegetable-stew/'

response = requests.get(recipe_url)

soup = BeautifulSoup(response.content, "html.parser")

title = soup.find("h1", {"class": "article-heading"})
print(title.text.strip())
ingredients = soup.findAll("li", {"class": "mntl-structured-ingredients__list-item"})
for ing in ingredients:
    x = ing.text.strip()
    # x = re.sub('[0123456789]', "", x) 
    # x = re.sub('[/.()]', "", x) 
    # x = re.sub('[¼]', "", x) 
    # x = re.sub('[½]', "", x)
    # x = re.sub('tablespoons', "", x) 
    # x = re.sub('cups', "", x)
    # x = re.sub('pound', "", x)  
    # x = re.sub('ounces', "", x) 
    # x = re.sub('ounce', "", x) 
    # x = re.sub('degrees F', "", x) 
    # x = re.sub('degrees C', "", x) 
    # x = x.strip()
    print(x)