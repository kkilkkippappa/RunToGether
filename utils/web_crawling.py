from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time

def crawl_marathon_reports(year: int, month: int):
    year_str = str(year)
    month_str = f"{year}{month:02d}"

    options = Options()
    options.add_argument("--headless")  # 디버깅 시에는 주석 처리
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("https://search.naver.com/search.naver?query=레포츠")
    time.sleep(3)  # 첫 페이지 로딩 대기

    max_pages = 10  # 최대 페이지 제한
    page_count = 1
    all_marathon_data = []
    seen_titles = set()

    try:
        # 날짜 선택: 전체 날짜 선택 버튼 클릭
        try:
            calendar_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.more_view"))
            )
            driver.execute_script("arguments[0].click();", calendar_button)
            time.sleep(1)
        except TimeoutException:
            print("날짜 선택 버튼 없음. 건너뜀.")

        # 연도 클릭
        try:
            year_elem = driver.find_element(By.XPATH, f"//li[@data-value='{year_str}']/a")
            driver.execute_script("arguments[0].click();", year_elem)
            time.sleep(1)
        except NoSuchElementException:
            print(f"연도 {year} 버튼 없음. 건너뜀.")

        # 월 클릭
        try:
            month_elem = driver.find_element(By.XPATH, f"//li[@data-value='{month_str}']/button")
            driver.execute_script("arguments[0].scrollIntoView(true);", month_elem)
            driver.execute_script("arguments[0].click();", month_elem)
            time.sleep(2)
        except NoSuchElementException:
            print(f"월 {month} 버튼 없음. 건너뜀.")

        # 마라톤 필터 클릭
        try:
            filter_buttons = driver.find_elements(By.XPATH, "//li[@role='tab']//button")
            for btn in filter_buttons:
                if "테마" in btn.text or "코스" in btn.text or "종목" in btn.text:
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                    break

            marathon_elem = driver.find_element(By.XPATH, "//li[@data-value='마라톤']/a")
            driver.execute_script("arguments[0].click();", marathon_elem)
            time.sleep(2)
        except NoSuchElementException:
            print("마라톤 필터 버튼 없음. 건너뜀.")

        # 페이지별 카드 데이터 수집 루프
        while True:
            print(f"{page_count} 페이지 수집 중...")

            # 카드 로드 대기
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card_item"))
                )
            except TimeoutException:
                print("카드 로딩 실패. 종료.")
                break

            soup = BeautifulSoup(driver.page_source, "html.parser")
            table_rows = soup.select("div.card_item")

            for row in table_rows:
                # 대회명
                title_tag = row.select_one("div.data_box div.title div.area_text_box strong.this_text a")
                
                # 날짜 & 장소 초기화
                date_tag = None
                loc_tag = None

                for dt in row.select("dl.rel_info dt"):
                    dd = dt.find_next_sibling("dd")
                    if dt.text.strip() == "기간":
                        date_spans = dd.select("span.info_date")
                        if len(date_spans) >= 2:
                            date1 = date_spans[0].text.strip()
                            date2 = date_spans[1].text.strip()
                            date_tag = f"{date1} ~ {date2}"
                        elif len(date_spans) == 1:
                            date_tag = date_spans[0].text.strip()
                    elif dt.text.strip() == "장소":
                        loc_tag = dd

                if title_tag and date_tag:
                    title_text = title_tag.text.strip()
                    if title_text not in seen_titles:
                        seen_titles.add(title_text)
                        all_marathon_data.append({
                            "대회명": title_text,
                            "날짜": date_tag,
                            "장소": loc_tag.text.strip() if loc_tag else ""
                        })

            # 종료 조건
            if page_count >= max_pages:
                print("최대 페이지 도달. 종료.")
                break

            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'btn_next')]//a"))
                )
                btn_display = next_button.value_of_css_property("display")
                if "none" in btn_display:
                    print("다음 버튼 비활성화 상태. 종료.")
                    break

                driver.execute_script("arguments[0].click();", next_button)
                page_count += 1
                time.sleep(2)
            except (TimeoutException, NoSuchElementException):
                print("다음 버튼 없음. 종료.")
                break

    finally:
        driver.quit()

    return all_marathon_data
