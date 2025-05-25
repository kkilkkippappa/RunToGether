import requests
import os, sys

class PaceModel:
    def __init__(self) -> None:
        self.pace_url = f"{os.getenv("SERVER_URL")}/pace/generate_plan"

    def fetch_generate_plan(self, data : dict):
            try:
                response = requests.post(self.pace_url, json=data)
                response.raise_for_status() #http 응답코드 받음. 
                return response.json()
            except requests.RequestException as e:
                 print(f"서버 요청 실패 : {str(e)}")
                 return {"error" : str(e)}
        