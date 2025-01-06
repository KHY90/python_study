import requests
from bs4 import BeautifulSoup

url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser",)

jobs = soup.find("section", class_ = "jobs").find_all("li") # class_ _를 붙여야 검색이 된다.

print(jobs)