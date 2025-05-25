import requests
import os

class MarathonModel:
    def __init__(self):
        self.base_url = os.getenv("SERVER_URL")
        self.marathon_url = f"{self.base_url}/marathon"
        self.marathon_url = f"{self.marathon_url}/get_crawling"
    
    def get_marathon_data(self):
        try:
            response = requests.get(self.marathon_url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"마라톤 데이터 조회 실패: {str(e)}")
            return []

    def get_crawled_marathon_data(self, year, month):
        try:
            #print(f'test용 {self.marathon_url}')
            response = requests.get(f'{self.marathon_url}?year={year}&month={month}')
            if response.status_code == 200:
                print(f"데이터 크롤링 성공!")
                return response.json()
                
            return None
        except Exception as e:
            print(f"마라톤 크롤링 데이터 조회 실패: {str(e)}")
            return e
