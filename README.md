# RunToGether 개요🏃‍♂️

RunToGether은 Kivy와 FastAPI를 기반으로 한 AI 러닝(마라톤) 보조 앱으로, 2025년 성균관대학교 러닝페어 출품작입니다.
GPS 기반 위치 정보와 기상청 날씨 데이터를 활용해 러닝 적합도를 판단하고, 
ChatGPT API를 통해 개인 맞춤형 페이스메이커 훈련 계획을 제공합니다.
최신 마라톤 대회 정보를 자동으로 크롤링해 제공합니다.

---
## 📌 주요 기능

- **GPS 위치 추적**: Plyer를 활용해 실시간 GPS 위치 확인
- **날씨 정보 조회**: 기상청 API를 통해 현재 위치의 기온, 습도, 강수 상태 조회 및 러닝 적합도 표시
- **페이스메이커 훈련 계획**: ChatGPT API를 사용해 목표 거리/시간/레벨 입력 후 주간 훈련 계획 생성
- **마라톤 대회 정보**: Selenium으로 크롤링한 최신 마라톤 대회 정보(대회명, 날짜, 장소) 제공
- **서버-앱 연동**: FastAPI 백엔드와 Kivy 앱 간 데이터 통신

## 📌 사용 기술
* Python (3.13)
* Kivy / KivyMD
* FastAPI
* Selenium
* ChatGPT API (OpenAI)
---
## ⚙️ 설치 및 실행 방법

### 1️⃣ Python 가상환경 설정

```bash
# 가상환경 생성
python -m venv [가상환경폴더명]
[예시]
python -m venv virtual_env
# (필요시) Python 3.13.3 버전 명시
python3.13 -m venv venv

(필요하다면 가상환경폴더로 이동)
(window) cd "가상환경폴더 절대경로"

# 가상환경 활성화 (Windows)
venv\Scripts\activate
# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
```
### 번외. 가상환경 비활성화
```bash
# 가상환경 비활성화 (Windows)
venv\Scripts\deactivate
# 가상환경 비활성화 (Mac/Linux)
source venv/bin/deactivate
```
### 2️⃣ 필수 패키지 설치
```bash
pip install -r requirements.txt
```
### 4️⃣ FastAPI 서버 실행
주의 : fastapi 서버실행은 타 cmd 창(가상환경 실행)에서 Run을 추천
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```
### 5️⃣ Kivy 앱 실행
```bash
python main.py
#아니면 IDE에서 실행
