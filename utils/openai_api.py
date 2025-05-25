from openai import OpenAI
import json



def get_gpt_data(race_distance, goal_time, experience_level, pace_min, pace_sec, recent_longest_distance, training_duration):
    client = OpenAI()
    message = [
    {"role": "system", "content": "You are a helpful assistant designed to output JSON format."},
    {"role": "user", "content": f"""
Race Distance: {race_distance} km
Goal: {goal_time}
Experience Level: {experience_level}
Pace: {pace_min}min {pace_sec}second
Recent Longest Distance: {recent_longest_distance} km
Training Duration: {training_duration} weeks
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
9. This is a list of json keys. Below are the key names and descriptions.
description : Runner level explanation and why we made this training and the target pace for each major training.
training_summary_table : List of training types and description of the pace by training type.
training_table: A training table for each week.
"""}
]
    model = "gpt-4o-mini"
    result = None
    for i in range(3):
        try:
            response = client.chat.completions.create(
            model = model,
            response_format = {"type": "json_object"},
            messages = message)
            result=json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"{i+1} 번째 시도 error")
            print(e)
            continue
        
    return result

# # 사용자 입력 변수 예시
# race_distance = 10  # km
# goal_time = "Finish only"  # "Finish only" 또는 "4:00:00" 형식
# experience_level = "초급"  # "초급", "중급", "상급"
# pace = 6  # min/km
# recent_longest_distance = 5  # km
# training_duration = 5  # weeks

# res = get_gpt_data(race_distance, goal_time, experience_level, pace, recent_longest_distance, training_duration)

# print(type(res))
# print(res['training_table'])
