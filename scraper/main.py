import requests
from bs4 import BeautifulSoup

all_jobs = []

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser",)
    jobs = soup.find("section", class_ = "jobs").find_all("li")[1:-1] # class_ _를 붙여야 검색이 된다.

    for job in jobs:
        title = job.find("span", class_="title").text
        company, position, region = job.find_all("span", class_="company")
        url = job.find("div", class_="tooltipn").next_sibling["href"]
        job_data = {
            "title": title,
            "company": company.text,
            "position": position.text,
            "region": region.text,
            "url": f"https://weworkremotely.com{url}"
        }
        all_jobs.append(job_data)

def get_pages(url):
    response = requests.get("https://weworkremotely.com/remote-full-time-jobs?page=1")
    soup = BeautifulSoup(response.content, "html.parser")
    return len(soup.find("div", class_="pagination").find_all("span", class_="page"))

total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")

for x in range(total_pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_page(url)

keywords = [
    "flutter",
    "python",
    "golang"
]

r = requests.get("https://remoteok.com/remote-flutter-jobs", header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"})

