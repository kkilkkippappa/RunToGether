from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os,sys
from openai import OpenAI
import json
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import logging


router = APIRouter(
    prefix="/pace",
)

#로거 세팅
logger = logging.getLogger("pacerouter")
logger.setLevel(logging.DEBUG)

#포맷터 설정
formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
#콘솔 핸들러
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# 각 핸들러를 로거에 추가
logger.addHandler(stream_handler)

class Plan(BaseModel):
    race_distance : float
    goal_time : str
    experience_level : str
    pace_min : int
    pace_sec : int
    recent_longest_distance : float
    training_duration : int

@router.post("/generate_plan")
async def generate_plan(data : Plan):
    client = OpenAI()
    message = [
    {"role": "system", "content": "You are a helpful assistant designed to output JSON format."},
    {"role": "user", "content": f"""
Race Distance: {data.race_distance} km
Goal: {data.goal_time}
Experience Level: {data.experience_level}
Pace: {data.pace_min}min {data.pace_sec}second
Recent Longest Distance: {data.recent_longest_distance} km
Training Duration: {data.training_duration} weeks
"""},
    {"role": "user", "content": "Please provide the output in JSON format, and translate English to Korean"},
    {"role": "assistant", "content": """
**Requirements for the Plan:**
1.  Present the output as a **week-by-week table**. Columns must include: **주차 #, 월, 화, 수, 목, 금, 토, 일** (showing workout type and distance/duration in kilometers for scheduled days, or "휴식" for non-selected days), and **주간 거리** (in kilometers).
2.  Ensure **gradual and sensible progression** of weekly mileage and the weekly long run distance.
3.  Intelligently distribute workout types.
4.  Include essential workouts: **Long Runs** (schedule strategically, considering weekend days if selected among training days), **Easy Runs**, and appropriate **Quality Sessions** (e.g., Tempo runs, Interval training, LSD) suitable for the specified Goal and Experience Level.
5.  Implement a standard **Taper Period** (reduced training volume) for the final 2-3 weeks before the race.
6.  **Please calculate and provide specific target training paces** (e.g., for Easy Runs, Long Runs, Tempo Runs, Interval Runs). **These paces are a required part of the output.** Ideally, include relevant paces directly within the weekly schedule descriptions (e.g., 'Tempo Run: 6 kilometers @ X:XX/kilometers pace') or list them clearly in a separate summary table accompanying the main schedule.
7.  The generated plan must be **systematic, internally consistent, and follow generally accepted training principles** suitable for preparing for a race.
8. Description of the Experience Level.
초급: Never run a full course marathon
중급: 1 full-course marathon run
상급: Running a full-course marathon several times
9. This is a list of json keys. Below are the key names and descriptions. json key name is available Korean;however, below json key list is used English.
description : Runner level explanation and why we made this training and the target pace for each major training.
training_summary_table : List of training types and description of the pace by training type.
training_table: A training table for each week.
"""}
]
    model = "gpt-4o-mini"
    result = None
    logger.info("init generate_plan")
    for i in range(3):
        try:
            response = client.chat.completions.create(
            model = model,
            response_format = {"type": "json_object"},
            messages = message, 
            timeout=120 #타임아웃 2분
            )
            result=json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            logger.error("{i+1} error : ", e)
            if i == 2:
                raise e
        