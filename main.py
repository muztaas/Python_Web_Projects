from flask import Flask, render_template
import requests
from datetime import date

app = Flask(__name__)


response = requests.get('https://saurav.tech/NewsAPI/top-headlines/category/health/in.json')
text = response.json()['articles']
year = date.today().year


@app.route('/')
def index():
    return render_template('news.html', txt=text, year=year)


@app.route('/blog/<num>')
def post(num):
    num = int(num)
    title = text[num]['title']
    author = text[num]['author']
    link = text[num]['url']
    context = text[num]['content'] or 'Content'
    desc = text[num]['description']
    if '[+' in context:
        context = context[:context.index('[+')]
    return render_template('blog.html', titl=title, auth=author, link=link, txt=context, desc=desc, year=year)


if __name__ == "__main__":
    app.run()

