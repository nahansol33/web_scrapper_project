import requests
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdrivermanager.chrome import ChromeDriverManager

def indeed_search(job_keyword):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.close()
    browser = webdriver.Chrome(options=options)
    results = []
    is_last_page = False
    i = 0
    while not is_last_page:
        # print(f"i right now is {i}")
        page_number = i * 10
        # base_url = f"https://ca.indeed.com/jobs?q={job_keyword}&l={location}&start={page_number}"
        base_url = f"https://ca.indeed.com/jobs?q={job_keyword}&start={page_number}"
        browser.get(base_url)
        response = browser.page_source
        soup = BeautifulSoup(response, "html.parser")
        indeed_verify = soup.find("body", class_="no-js")
        if indeed_verify != None:
            print("security check")
        pagination = soup.find("nav", class_="css-jbuxu0 ecydgvn0")
        job_results = soup.find("ul", class_="css-zu9cdh eu4oa1w0")
        browser.implicitly_wait(40)
        jobs = job_results.find_all("li", recursive=False)
        # print("number of jobs in this page is" + str(len(jobs)))
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone nonJobContent-desktop")
            if zone == None:
                anchor = job.select_one("h2 a")
                job_link = "https://" + anchor["href"]
                job_title = job.find("h2", class_="jobTitle").string.replace(",", " ")
                company = job.find("span", class_="companyName").string.replace(",", " ")
                location = job.find("div", class_="companyLocation").string
                if location != None:
                    location = location.replace(",", " ")
                else:
                    location = "No location specified"
                job_data = {
                    "link": job_link,
                    "title": job_title,
                    "company": company,
                    "location": location
                }
                results.append(job_data)
        if pagination == None or i >= 6:
            print("pagination is none")
            is_last_page = True
        else:
            print("pagination exists")
            pagination_divs = pagination.find_all("div", class_="css-tvvxwd ecydgvn1")
            last_div = pagination_divs[-1]
            if last_div.find("button") == None:
                print("you are not on the last page")
                is_last_page = False
            else:
                is_last_page = True
        i += 1
        # print(i)
    browser.close()
    return results

