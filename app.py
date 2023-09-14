from flask import Flask, render_template, request
from terminalversion import get_recipe_urls, calculate_most_common, scrape_recipe_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eta', methods=['POST'])
def eta():
    page_url = request.form['url']
    #check if page_url is valid allrecipes link
    if page_url is None:
        page_url = 'https://www.allrecipes.com/recipes/17562/dinner/'

    recipe_urls = get_recipe_urls(page_url)
    etatime = 0.33 * len(recipe_urls)
    etatime = '%.2f' % etatime
    return render_template('eta.html', etatime = etatime, len = len(recipe_urls), url = page_url)

@app.route('/predefinedeta', methods=['GET'])
def predefinedeta():
    page_url = 'https://www.allrecipes.com/recipes/17562/dinner/'

    recipe_urls = get_recipe_urls(page_url)
    etatime = 0.33 * len(recipe_urls)
    etatime = '%.2f' % etatime
    return render_template('eta.html', etatime = etatime, len = len(recipe_urls), url = page_url)

@app.route('/results')
def results():
    page_url = request.args.get('url')

    all_ingredients = []
    titles = []
    recipe_urls = get_recipe_urls(page_url)
    for recipe_url in recipe_urls:
        title, ingredients = scrape_recipe_data(recipe_url)
        titles.append(title)
        all_ingredients.extend(ingredients)
    
    common_ingredients = calculate_most_common(all_ingredients)

    return render_template('results.html', url=page_url, ingredients=common_ingredients)

if __name__ == '__main__':
    app.run(debug=True)

