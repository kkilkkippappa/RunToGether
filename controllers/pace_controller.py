class PaceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def generate_plan(self, distance, week, goal_hour, goal_min, pace_min, pace_sec, max_distance, level):
        try:
            goal_time = f"{int(goal_hour)} hour {int(goal_min)} minute"  
            # 타입 변환 (서버 API 요구에 맞춤)
            data = {
                "race_distance": float(distance),
                "goal_time" : goal_time, 
                "experience_level": level,  # 문자열 그대로 유지
                "pace_min": int(pace_min),
                "pace_sec": int(pace_sec),
                "training_duration": float(max_distance),
                "recent_longest_distance": int(week)
            }

            response = self.model.fetch_generate_plan(data)

            if not response:
                return {"error": "서버에서 데이터를 받아오지 못했습니다."}

            if isinstance(response, dict) and response.get("error"):
                return {"error": response["error"]}

            return response

        except ValueError as e:
            return {"error": f"입력값 변환 오류: {str(e)}"}
        except Exception as e:
            return {"error": f"요청 중 오류 발생: {str(e)}"}
