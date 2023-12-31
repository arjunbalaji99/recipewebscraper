import re
import requests
import random
import time
from collections import Counter
from bs4 import BeautifulSoup

#given an allrecipes page - returns all recipe urls on the page
def get_recipe_urls(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    all_urls = soup.findAll("a", {"class": "mntl-card-list-items"})
    
    recipe_urls = []

    for a in all_urls:
        url = a['href']
        if any(chr.isdigit() for chr in url):
            recipe_urls.append(url)
    
    return recipe_urls

def select_preselected_url():
    preselected_urls = ["https://www.allrecipes.com/recipes/17561/lunch/", "https://www.allrecipes.com/recipes/84/healthy-recipes/", "https://www.allrecipes.com/recipes/76/appetizers-and-snacks/", "https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/"]
    return preselected_urls[random.randint(0, len(preselected_urls) - 1)]


#cleans up ingredient data to just the ingredient (removes all numbers, measurements, etc) - return cleaned ingredient
def cleans_data(ingredient):
    ingredient = ingredient.text.strip()
    ingredient = re.sub('[0123456789]', "", ingredient) 
    ingredient = re.sub('[/.()]', "", ingredient) 
    ingredient = re.sub('[¼]', "", ingredient) 
    ingredient = re.sub('[½]', "", ingredient)
    ingredient = re.sub('tablespoons', "", ingredient)
    ingredient = re.sub('tablespoon', "", ingredient)
    ingredient = re.sub('teaspoons', "", ingredient) 
    ingredient = re.sub('teaspoon', "", ingredient) 
    ingredient = re.sub('cups', "", ingredient)
    ingredient = re.sub('cup', "", ingredient)
    ingredient = re.sub('pounds', "", ingredient)
    ingredient = re.sub('pound', "", ingredient)  
    ingredient = re.sub('ounces', "", ingredient) 
    ingredient = re.sub('ounce', "", ingredient) 
    ingredient = re.sub('degrees F', "", ingredient)
    ingredient = re.sub('degrees C', "", ingredient)
    ingredient = ingredient.strip()
    
    return ingredient

#given a recipe page url - returns all cleaned ingredients from that recipe
def scrape_recipe_data(recipe_url):
    response = requests.get(recipe_url)
    soup = BeautifulSoup(response.content, "html.parser")
    ingredients = []

    title = soup.find("h1", {"class": "article-heading"})
    title = title.text.strip()
    scraped_ingredients = soup.findAll("li", {"class": "mntl-structured-ingredients__list-item"})
    for ingredient in scraped_ingredients:
        ingredients.append(cleans_data(ingredient))

    return title, ingredients

#calculates and prints the 10 most common ingredients from a list of ingredients
def calculate_most_common(all_ingredients):
    return Counter(all_ingredients).most_common(10)

#prints the most common ingredients in a neat format
def print_most_common(most_common_ingredients):
    for ingredient in most_common_ingredients:
        print(str(ingredient[0]).capitalize() + " - " + str(ingredient[1]) + " occurrences")

#calculates eta of scraping given a list of recipe urls
def calculate_eta(recipe_urls):
    etatime = 0.33 * len(recipe_urls)
    etatime = '%.2f' % etatime
    return etatime

#handles all interaction with the user
def user_interaction():
    print("Hello! Welcome to the Recipe Scraping Ingredient Compiler!")
    page_url = input("If you have a specific recipes page you would like to scrape, input it here! If you do not, that is fine and we can just use one of our pre-selected pages - type NONE in that scenario!")
    time.sleep(1)
    if page_url == 'NONE':
        page_url = select_preselected_url()
        print("This is the page that will be scraped: " + page_url)

    all_ingredients = []
    titles = []
    recipe_urls = get_recipe_urls(page_url)
    time.sleep(2)
    print("Scraping " + str(len(recipe_urls)) + " recipes...")
    eta = calculate_eta(recipe_urls)
    time.sleep(1)
    print("ETA: " + str(eta) + " seconds")
    for recipe_url in recipe_urls:
        title, ingredients = scrape_recipe_data(recipe_url)
        titles.append(title)
        all_ingredients.extend(ingredients)
    
    print("Here are the 10 most common ingredients of the recipes on that page!")
    most_common_ingredients = calculate_most_common(all_ingredients)
    print_most_common(most_common_ingredients)

if __name__ == "__main__":
    user_interaction()