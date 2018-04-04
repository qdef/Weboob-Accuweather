# Weboob-Accuweather

Weboob module using the CapWeather capability to scrap weather data from accuweather.com

Please note that this module has been developed for the <b>1.4 version of Weboob</b>.
  
<h2> How to setup the accuweather module in weboob</h2>

1- First you need to add this module in your <b>Weboob modules folder</b>.

2- In your terminal you must type <b>'weboob-config update'</b> and verify that the Accuweather module has been correctly installed.

3- Open the weather application by typing <b>'wetboobs'</b> in your terminal.

4- If no weather backends are previously installed, wetboobs will offer you to install backends. If you did the previous steps correctly, the accuweather module should appear in the backends list.

5- If other weather backends are already installed, you may use the <b>'backends add accuweather'</b> to add the accuweather module. You can also use <b>'backends remove [backendname]'</b> to uninstall a backend.
  
<h2> How to use the accuweather module in weboob</h2>

This module contains three functions: <b>cities, current and forecast</b>.

<h3>Search a city</h3>

Simply type <b>'cities [cityname]'</b> in the wetboobs terminal after installing the accuweather module.
If your input corresponds to existing cities, wetboobs should return you with a list of cities.
 
<b>Example:</b>
'cities york'

<b>wetboobs returns:</b>

1 — York - York, United Kingdom (accuweather)

2 — York - Ontario, Canada (accuweather)

3 — York University Heights - Ontario, Canada (accuweather)

4 — York - Pennsylvania, United States (accuweather)

5 — York Mills - Ontario, Canada (accuweather)

6 — Yorkdale-Glen Park - Ontario, Canada (accuweather)

7 — Yorkton - Saskatchewan, Canada (accuweather)

8 — Yorkville - Illinois, United States (accuweather)

9 — York - Westmoreland, Jamaica (accuweather)

10 — York - Nebraska, United States (accuweather)

 
 
<h3>Get current weather data of a city</h3>

After the city search, simply type <b>'current [city_ID]'</b> in the wetboobs terminal, city_ID being the figure preceding the name of your city of interest.
In the former example, if we want to know the weather in York, United Kingdom, we would type 'current 1'.

<b>wetboobs returns:</b>

2018-04-03: 14 °C -  Real Feel: 12° - Clouds and sun - Wind speed: 21 km/h - Humidity: 59% - Pressure: 988.00 mb ↓ - UV index: 2 - Cloud cover: 60%.

 
 
<h3>Get the weather forecast of a city</h3>

Type <b>'forecasts [city_ID]'</b> in your terminal (for example, 'forecasts 1') and you will get the weather forecast of the four next days.

<b>wetboobs returns:</b>

* Wed  Apr 4:     (0 °C - 12 °C) - A couple of p.m. t-showers

* Thu  Apr 5:     (3 °C - 11 °C) - Sunshine mixing with clouds

* Fri  Apr 6:     (7 °C - 13 °C) - Cloudy

* Sat  Apr 7:     (5 °C - 15 °C) - A couple of showers


If you have any questions on this module, feel free to contact me at:

quentin.defenouillere@gmail.com








