import requests
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdrivermanager.chrome import ChromeDriverManager
from flask import Flask, render_template, request, redirect, send_file
from extractor import *

from wwr import *
from indeed import *
from file import *

# def linked_in_search(job_keyword, location):
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("detach", True)
#     driver = webdriver.Chrome(options=options)
#     base_url = f"https://www.linkedin.com/jobs/search/?currentJobId=3693013360&geoId=100025096&keywords={job_keyword}&location={location}"
#     response = get(base_url)
#     driver = webdriver.Chrome()
#     driver.get(base_url)

# linked_in_search("python", "toronto")

app = Flask("JobScrapper")
db = {}

@app.route("/")
def home():
    return render_template("home.html", name="Hola")

@app.route("/hello")
def hello():
    return "Hello You!"

@app.route("/search")
def search():
    searchWord = request.args["searchWord"]
    if searchWord is "" or searchWord == None:
        return redirect("/")
    else:
        if searchWord in db:
            jobs = db[searchWord]
        else:
            jobs = job_extractor(searchWord)
            db[searchWord] = jobs
        # save_to_file("java_jobs", search_results)
        return render_template("search.html", jobs = jobs, searchWord = searchWord)

@app.route("/export")
def export():
    searchWord = request.args["searchWord"]
    if searchWord == None:
        return redirect("/")
    if searchWord not in db:
        return redirect(f"/search?searchWord={searchWord}")
    else:
        save_to_file(searchWord, db[searchWord])
    return send_file(f"{searchWord}.csv", as_attachment=True)
app.run("127.0.0.1")