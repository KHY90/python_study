from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


def scrape_jobs(keyword):
    with sync_playwright() as p:
        # 브라우저 실행
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 사이트 접속
        page.goto("https://www.wanted.co.kr/jobsfeed")
        time.sleep(5)  # 속도 조절을 위해 대기

        # 검색 버튼 클릭
        page.click("button.Aside_searchButton__rajGo")
        time.sleep(5)

        # 검색어 입력
        page.get_by_placeholder("검색어를 입력해 주세요.").fill(keyword)
        time.sleep(5)

        # Enter 키 입력
        page.keyboard.down("Enter")
        time.sleep(5)

        # 검색 결과 탭 클릭
        page.click("a#search_tab_position")
        time.sleep(5)

        # 페이지 끝까지 스크롤
        for _ in range(5):
            time.sleep(5)
            page.keyboard.down("End")

        # 페이지 소스 가져오기
        content = page.content()
        browser.close()

    # BeautifulSoup으로 데이터 파싱
    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_="JobCard_container__REty8")

    # 크롤링한 데이터 저장
    jobs_db = []
    for job in jobs:
        link_tag = job.find("a")
        title_tag = job.find("strong", class_="JobCard_title__HBpZf")
        company_tag = job.find("span", class_="JobCard_companyName__N1YrF")
        reward_tag = job.find("span", class_="JobCard_reward__oMh8L")

        link = f"https://www.wanted.co.kr{link_tag['href']}" if link_tag else "No Link"
        title = title_tag.text if title_tag else "No Title"
        company_name = company_tag.text if company_tag else "Unknown Company"
        reward = reward_tag.text if reward_tag else "No Reward"

        job_data = {
            "title": title,
            "company_name": company_name,
            "reward": reward,
            "link": link,
        }
        jobs_db.append(job_data)

    # 데이터를 각 키워드에 맞는 CSV 파일에 저장
    file_name = f"jobs_{keyword}.csv"
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Reward", "Link"])
        for job in jobs_db:
            writer.writerow(job.values())

if __name__ == "__main__":
    # 키워드 리스트
    keywords = ["flutter", "nextjs", "kotlin"]

    # 각 키워드에 대해 크롤링 실행
    for keyword in keywords:
        scrape_jobs(keyword)
