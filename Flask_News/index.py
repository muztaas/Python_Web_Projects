""" A project which uses NewsAPI to fetch current/recent news """

from flask import Flask, render_template, request
import requests
from datetime import date

apikey = '869223720a7c486c8295b3b0e827ee8f'
website = 'https://newsapi.org/v2/'

countries = ['us', 'in', 'ch', 'jp', 'ca', 'gb']
year = date.today().year

response = []

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_index():
    display = 0
    if request.method == 'POST':
        global response
        if (country := request.form.get('in')) in countries:
            url = website + 'top-headlines?country=' + country + '&apiKey=' + apikey
            response = requests.get(url).json()['articles']
            return render_template('news.html', txt=response, year=year)
        elif request.form.get('textbox') is not None:
            keyword = request.form['textbox']
            url = website + 'everything?q=' + keyword + '&apiKey=' + apikey
            response = requests.get(url).json()['articles']
            return render_template('news.html', txt=response, year=year)
        elif request.form.get('dropdown') == 'keyword':
            display = 1
        elif request.form.get('dropdown') == 'country':
            display = 2

    return render_template('news_selection.html', hide=display, year=year)


@app.route('/blog/<num>')
def post(num):
    num = int(num)
    title = response[num]['title'] or 'Title'
    author = response[num]['author'] or 'Author'
    description = response[num]['description'] or 'Description'
    text = response[num]['content'] or 'Content'
    url = response[num]['url'] or 'URL'
    return render_template('blog.html', titl=title, auth=author, desc=description, txt=text, link=url, year=year)


@app.route('/about')
def about_us():
    return render_template('about_us.html')


if __name__ == '__main__':
    app.run()
