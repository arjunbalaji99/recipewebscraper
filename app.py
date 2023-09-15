from flask import Flask, render_template, request
from terminalversion import get_recipe_urls, calculate_most_common, scrape_recipe_data, calculate_eta, select_preselected_url

#builds flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')

#routes to home page - basic template
@app.route('/')
def index():
    return render_template('index.html')

#routes to a page where it displays the eta - makes it less frustrating when it loads for ages
@app.route('/eta', methods=['POST'])
def eta():
    page_url = request.form['url']

    recipe_urls = get_recipe_urls(page_url)
    return render_template('eta.html', etatime = calculate_eta(recipe_urls), len = len(recipe_urls), url = page_url)

#if user chooses a predefined url
@app.route('/predefinedeta')
def predefinedeta():
    page_url = select_preselected_url()

    recipe_urls = get_recipe_urls(page_url)
    return render_template('eta.html', etatime = calculate_eta(recipe_urls), len = len(recipe_urls), url = page_url)

#calculates and displays users results
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

