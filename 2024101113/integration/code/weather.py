class WeatherModule:
    def __init__(self):
        self.current_weather = "Clear"

    def set_weather(self, weather):
        self.current_weather = weather
        return f"Weather set to {weather}."

