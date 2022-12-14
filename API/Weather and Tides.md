# Weather and Tides

### Data

last_update:  datetime

##### sensor

temp_inside

temp_outside

barometric_pressure

humidity



##### API

tide_dict (tide1, tide2, tide3, tide4, tide5,  for each: {time: datetime, type: high, level: 13.4})



##### derived

dew_point

wind_chill

wind_speed

rain_hour_dict   (list of hourly rains for the day, 24hour:inches)

rain_today   (sum of rain_hour_list)

rain_day_dict  (list of daily rain for month, date:inches)





### News Headlines:  NYT

allensxx5@gmail.com

Pass:  dogsINspace367$

dev portal:  https://developer.nytimes.com/?it=a

top stories:  https://developer.nytimes.com/docs/top-stories-product/1/overview

### Tides

NOAA CO-OP

* documentation:  https://api.tidesandcurrents.noaa.gov/api/prod/
* tide stations numbers
  * Washington:  https://tidesandcurrents.noaa.gov/tide_predictions.html?gid=1415
  * All:  https://tidesandcurrents.noaa.gov/tide_predictions.html
  * 

Arletta:  9446491

URL:

```
url = 'https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&interval=hilo&format=json&units=metric&time_zone=lst_ldt&station=9446491'
```

#### URL with f-string

```
url = f'https://tidesandcurrents.noaa.gov/api/datagetter?begin_date={begin_date}&range={time_range}&product={product}\
&datum=mllw&interval={interval}&format=json&units={units}&time_zone=lst_ldt&station={station}'

url = "&".join(('https://tidesandcurrents.noaa.gov/api/datagetter?time_zone=lst_ldt',
    f'station={station}',
    f'begin_date={begin_date}',
    f'range={time_range}',
    'product=predictions',
    'datum=mllw',
    'interval=hilo',
    'format=json',
    'units=metric',
    ))
```



```
result:
('{ "predictions" : [\n'
 '{"t":"2022-11-10 00:00", "v":"-1.710", "type":"L"},{"t":"2022-11-10 07:18", '
 '"v":"13.797", "type":"H"},{"t":"2022-11-10 12:50", "v":"7.468", '
 '"type":"L"},{"t":"2022-11-10 17:22", "v":"12.269", '
 '"type":"H"},{"t":"2022-11-11 00:34", "v":"-1.672", '
 '"type":"L"},{"t":"2022-11-11 08:01", "v":"13.869", '
 '"type":"H"},{"t":"2022-11-11 13:40", "v":"7.926", '
 '"type":"L"},{"t":"2022-11-11 17:54", "v":"11.601", '
 '"type":"H"},{"t":"2022-11-12 01:11", "v":"-1.365", '
 '"type":"L"},{"t":"2022-11-12 08:44", "v":"13.767", '
 '"type":"H"},{"t":"2022-11-12 14:36", "v":"8.163", '
 '"type":"L"},{"t":"2022-11-12 18:30", "v":"10.885", "type":"H"}\n'
 ']}\n')
```



## Weather

Nice wind and pressure overlay:  https://www.windy.com/-Show---add-more-layers/overlays?pressure,49.131,-117.784,6,i:pressure,m:eTUadlh





### National Weather Service

Weather forecast API:  https://www.weather.gov/documentation/services-web-api

Hourly?  https://www.weather.gov/wrn/hourly-weather-graph

this returns the grid location using lat/long:  url = 'https://api.weather.gov/points/39.7456,-97.0892'

### Openweathermap API

openweathermap.org

docs on the output:  https://openweathermap.org/current

To find city codes, go to openweathermap.org and search city (City Name, US).  The code will be in the URL. Or can download list here:  http://bulk.openweathermap.org/sample/

Fort Wayne:  4920423
Columbia City:  4919203
Tacoma:  5812944
Gig Harbor:  5795440
