from datetime import datetime
from fastapi import APIRouter, HTTPException, Query

from pydantic import BaseModel
from typing import List

import os,sys
from dotenv import load_dotenv
import logging
import requests
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.web_crawling import crawl_marathon_reports

# .env 파일 불러오기
load_dotenv()

# 환경변수 불러오기
weather_api_key = os.getenv("WEATHER_API_KEY")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # 필요시 DEBUG

# 라우터 설정 : weather
router = APIRouter(
    prefix="/marathon",
)

class MarathonData(BaseModel):
    대회명 : str
    날짜 : str
    장소 : str

@router.get('/get_crawling', response_model=List[MarathonData])
async def get_crawling(year:int = Query(..., description="연도"), month:int  = Query(..., description='월(1~12)')):
    try:
        res = crawl_marathon_reports(year, month)
        return res
    except Exception as e:
        logger.info(f"오류발생 : {e}")
        return {{"대회명": "오류 발생", "날짜": "", "장소": str(e)}}