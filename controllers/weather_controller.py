class WeatherController:
    def __init__(self, model, view):
        self.model = model
        self.view = view


    def update_weather_data(self):
        data = self.model.get_weather_data()
        if data:
            weather_status = self.model.is_good_weather_to_running()
            self.view.update_weather_display(data, weather_status)
        else:
            self.view.update_weather_display(None, None)

    def send_location(self, lat, lon):
        result = self.model.send_location(lat, lon)
        if result and result.get("status") == "success":
            self.update_weather_data()
        else:
            self.view.update_weather_display(None, None)
        return result

    