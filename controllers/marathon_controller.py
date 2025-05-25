class MarathonController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def update_marathon_data(self):
        print("update_marathon_data start")
        data = self.model.get_marathon_data()
        self.view.update_marathon_display(data or [])

    def search_marathons(self, year, month):
        """연도와 월로 마라톤 데이터 검색 (API 요청)"""
        try : 
            print("search_marathons start")
            data = self.model.get_crawled_marathon_data(year, month)

            # 데이터 Key 이름 매핑
            for item in data:
                item["일시"] = item.pop("날짜", "-")

            columns = ['대회명', '일시', '장소']
            self.view.update_table(data or [], columns)
        except Exception as e:
            self.view.show_error(f"데이터 조회 실패 : ", {str(e)})
