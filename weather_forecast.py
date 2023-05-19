from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import api_key as api

def weather_forecast():
    owm = OWM(api.API_KEY)
    mgr = owm.weather_manager()
    reg = owm.city_id_registry()
    one_call = mgr.one_call(lat=53.90026, lon=-9.60260)
    # Search for current weather in London (Great Britain) and get details
    observation = mgr.weather_at_place('Newport, IE')
    w = observation.weather

    print(w.detailed_status)        # 'clouds'
    print(w.wind())                  # {'speed': 4.6, 'deg': 330}
    print(w.humidity)                # 87
    print(w.temperature('celsius'))  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    print(w.rain)    
    for forecast_weather in one_call.forecast_daily:
        print(f"TEMPERATURES{forecast_weather.temperature('celsius')}")
        print(f"WIND{forecast_weather.wind()}")
        print(f"WIND{forecast_weather.wind()}")
        print(f"FORECAST{forecast_weather}")
    # print(one_call.forecast_daily[0].temperature('celsius'))
    # list_of_tuples = reg.ids_for('Newport', 'IE', matching='like')
    # print(list_of_tuples) 