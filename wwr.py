import requests
from requests import get
from bs4 import BeautifulSoup

def extract_jobs(job_keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?search_uuid=&term="
    search_term = job_keyword
    search_url = base_url + search_term
    response = get(search_url)
    if not response.status_code == 200:
        print(f"Can't connect to {search_url}")
    else:
        job_results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        for job in jobs:
            job_posts = job.find_all("li")
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all("a")
                job_link = anchors[1]
                link = job_link["href"]
                company, kind, region = job_link.find_all("span", class_="company")
                title = job_link.find("span", class_="title")
                job_data = {
                    "link": "https://" + link,
                    "title": title.string.replace(",", " "),
                    "company": company.string.replace(",", " "),
                    "location": region.string.replace(",", " ")
                }
                job_results.append(job_data)
        return job_results