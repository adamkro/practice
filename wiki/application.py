import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
import time
import random

app = Flask(__name__, template_folder=r"C:\Users\adamk\gitpractice\practice\wiki")


def wiki_article(article):
    # get wikipage of a specific article
    url = 'https://en.wikipedia.org/wiki/' + article
    webpage_response = requests.get(url)
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    return soup, url


def get_first_img_src(soup):
    # get first SIGNIFICANT image with width bigger than 50
    for n in range(5):
        img = soup.find_all("img")[n]
        img_width = img.get('width')
        if int(img_width) > 50:
            img_src = img.get('src')
            return img_src
    # no big img found, return first
    img_src = soup.img.get('src')
    return img_src


def get_categories(soup):
    # get soup categories
    try:
        categories_data = soup.select('.mw-normal-catlinks > ul')[0]
    except IndexError:
        return ["No tags available"]
    categories = (categories_data.get_text('|')).split('|')
    return categories


def related_to_categories(subject, categories):
    subject = subject.lower()
    for category in categories:
        if subject in category.lower():
            return True
    return False


def get_head(soup):
    # get heading
    return soup.select("#firstHeading")[0].string


def get_paragraph_text(soup):
    # get first SIGNIFICANT paragraph (longer than 20)
    n = 0
    p = soup.select('.mw-parser-output > p')[n]
    p_text = p.get_text()
    while len(p_text) < 20:
        n += 1
        p = soup.select('.mw-parser-output > p')[n]
        p_text = p.get_text()
    return p_text


def rand_article():
    rand_url = "https://en.wikipedia.org/wiki/Special:Random"
    webpage_response = requests.get(rand_url)
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    return soup

def rand_article_by_category(subject):
    rand_url = "https://en.wikipedia.org/wiki/Special:RandomInCategory/" + subject.replace(" ", "_")
    print("rand url: ", rand_url)
    webpage_response = requests.get(rand_url)
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    return soup


def generate_url_by_head(head):
    url = 'https://en.wikipedia.org/wiki/' + head.replace(" ", "_")
    return url


def get_sub_pages(soup):
    pages = soup.select(".mw-category-group > ul > li > a")
    return pages


def rand_inner_page(soup):
    pages = get_sub_pages(soup)
    try:
        ran_page = random.choice(pages)
    except IndexError:
        raise NameError("Category has no subpages")
    page_url = ran_page['href']
    article = "https://en.wikipedia.org" + page_url
    return wiki_article(article)

def is_category(head):
    if head == "Random page in category":
        raise NameError('No such category')
    elif "Category:" in head:
        return True
    return False


@app.route("/", methods=["POST", "GET"])
def random_page():
    subject = request.form.get("subject")
    t0 = time.perf_counter()
    if subject is None:
        return render_template("index.html")
    else:
        soup = rand_article_by_category(subject)
        head = get_head(soup)
        print("First head: " ,head)
        if is_category(head):
            #entered a sub category
            soup, wiki_url = rand_inner_page(soup)
            print("wiki url: ", wiki_url)
        else:
            wiki_url = generate_url_by_head(head)
            print("else wikiurl: ", wiki_url)

        categories = get_categories(soup)
        img_src = get_first_img_src(soup)
        text = get_paragraph_text(soup)
        t1 = time.perf_counter()
        elapsed_time = round(t1-t0, 2)
        return render_template("index.html", head=head, img_src=img_src,
                               categories=categories, text=text,
                               wiki_url=wiki_url, elapsed_time=elapsed_time)


@app.route("/<string:article>", methods=["POST", "GET"])
def index(article):
    soup, wiki_url = wiki_article(article)
    head = get_head(soup)
    img_src = get_first_img_src(soup)
    text = get_paragraph_text(soup)
    categories = get_categories(soup)
    return render_template("index.html", head=head, img_src=img_src,
                           categories=categories, text=text, wiki_url=wiki_url)


if __name__ == "__main__":
    app.debug = True
    app.run()

'''
webpage_response = requests.get("https://en.wikipedia.org/wiki/Category:Economic_history")
webpage = webpage_response.content
soup = BeautifulSoup(webpage, "html.parser")
#print(get_head(soup))
#print(get_paragraph_text(soup))
#print(get_categories(soup))

def get_sub_categories(soup):
    sub_categories = soup.select(".CategoryTreeItem > a")
    return sub_categories

def page_or_sub_category(soup):
    pages = get_sub_pages(soup)
    sub_categories = get_sub_categories(soup)
    if random.randint(0,1) == 0:
        #50% precent chance
        chosen_articles = pages
    else:
        chosen_sub_category = random.choice(sub_categories)
        sub_category_url = "https://en.wikipedia.org" + chosen_sub_category.['href']
        webpage_response = requests.get(sub_category_url)
        webpage = webpage_response.content
        sub_soup = BeautifulSoup(webpage, "html.parser")
        chosen_articles = get_sub_pages(sub_soup)
'''
