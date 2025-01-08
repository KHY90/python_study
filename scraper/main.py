import requests
from bs4 import BeautifulSoup

class JobScraper:
    def __init__(self, base_url, keywords=None):
        self.base_url = base_url
        self.keywords = keywords if keywords else []
        self.all_jobs = []

    def get_total_pages(self):
        """
        페이지네이션을 위한 총 페이지 수
        """
        response = requests.get(f"{self.base_url}?page=1")
        soup = BeautifulSoup(response.content, "html.parser")
        pagination = soup.find("div", class_="pagination")
        if not pagination:
            return 1  # 페이지네이션이 없으면 기본값으로 1 반환
        return len(pagination.find_all("span", class_="page"))

    def scrape_page(self, url):
        """
        단일 페이지에서 채용 공고를 크롤링하여 all_jobs에 추가
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs_section = soup.find("section", class_="jobs")
        if not jobs_section:
            return  # 채용 섹션이 없으면 스킵

        jobs = jobs_section.find_all("li")[1:-1]
        for job in jobs:
            title = job.find("span", class_="title").text if job.find("span", class_="title") else "No Title"
            company = job.find("span", class_="company").text if job.find("span", class_="company") else "Unknown Company"
            region = job.find("span", class_="region").text if job.find("span", class_="region") else "Unknown Region"
            url_tag = job.find("a")
            job_url = f"https://weworkremotely.com{url_tag['href']}" if url_tag else "No URL"

            job_data = {
                "title": title,
                "company": company,
                "region": region,
                "url": job_url,
            }
            self.all_jobs.append(job_data)

    def scrape_all_pages(self):
        """
        총 페이지 수를 기준으로 모든 페이지에서 데이터를 크롤링
        """
        total_pages = self.get_total_pages()
        for page in range(1, total_pages + 1):
            url = f"{self.base_url}?page={page}"
            self.scrape_page(url)

    def filter_jobs(self):
        """
        키워드를 기준 채용 공고 필터터
        """
        if not self.keywords:
            return self.all_jobs  # 키워드가 없으면 모든 공고를 반환
        filtered_jobs = [
            job for job in self.all_jobs
            if any(keyword.lower() in job["title"].lower() for keyword in self.keywords)
        ]
        return filtered_jobs


if __name__ == "__main__":
    base_url = "https://weworkremotely.com/remote-full-time-jobs"
    keywords = ["flutter", "python", "golang"]

    scraper = JobScraper(base_url, keywords)
    scraper.scrape_all_pages()
    filtered_jobs = scraper.filter_jobs()

    # 필터링된 채용 공고
    for job in filtered_jobs:
        print(job)
