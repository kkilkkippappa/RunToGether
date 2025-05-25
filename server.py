from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# api router 파일들
from fastapi_server.weather_router import router as weather_router
from fastapi_server.pace_router import router as pace_router
from fastapi_server.marathon_router import router as marathon_router

load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather_router) # 날씨 관련 
app.include_router(pace_router) # 마라톤 페이스 계산 라우터
app.include_router(marathon_router) #마라톤 대회 리스트 라우터

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=["server"]) 