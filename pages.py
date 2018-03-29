# -*- coding: utf-8 -*-

# Copyright(C) 2018      qdef
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from datetime import date
from weboob.browser.pages import JsonPage, HTMLPage
from weboob.browser.elements import ItemElement, ListElement, DictElement, method
from weboob.capabilities.base import NotAvailable
from weboob.capabilities.weather import Forecast, Current, City, Temperature
from weboob.browser.filters.json import Dict
from weboob.browser.filters.standard import CleanText, CleanDecimal, Regexp, Format, Eval, Env

__all__ = ['SearchCitiesPage', 'WeatherPage']


class SearchCitiesPage(JsonPage):
    @method
    class iter_cities(DictElement):
        ignore_duplicate = True

        class item(ItemElement):
            #Using the Accuweather search API to get the city IDs from the pattern search
            klass = City
            # 'Key' corresponds to the city ID that is used to create the URL of one specific city:
            obj_id = Dict('Key')
            # Formatting the city name with its region and country in case the searched pattern returns identical city names in different countries (example: 'York')
            obj_name = Format(u'%s - %s, %s', Dict('LocalizedName'), Dict['AdministrativeArea']['LocalizedName'], Dict['Country']['LocalizedName'])

class WeatherPage(HTMLPage):
    @method
    class get_current(ItemElement):
        klass = Current
        obj_id = Env('city_id2')
        obj_date = date.today()
        
        # Formatting weather data from the city of interest:
        obj_text = Format(' Real Feel: %s - %s - Wind speed: %s - Humidity: %s - Pressure: %s - UV index: %s - Cloud cover: %s.',
                          CleanText('//div[@class="lt"]//tbody/tr[3]/td/text()'), #Real Feel
                          CleanText('//div[@id="details"]//span[@class="cond"]/text()'), #Weather condition
                          CleanText('//ul[@class="stats"]/li[2]/strong/text()'), #Wind speed
                          CleanText('//ul[@class="stats"]/li[3]/strong/text()'), #Humidity
                          CleanText('//ul[@class="stats"]/li[4]/strong/text()'), #Pressure
                          CleanText('//ul[@class="stats"]/li[5]/strong/text()'), #UV index
                          CleanText('//ul[@class="stats"]/li[6]/strong/text()')) #Cloud cover

        def obj_temp(self):
            #Retrieving the temperature:
            temp = CleanText('//div[@id="details"]//span[@class="large-temp"]/text()')(self)
            #Eliminating the '°' at the end of the temperature value:
            temp=temp[:-1]
            temp = CleanDecimal(temp)(self)
            
            #Retrieving the temperature unit in Celsius or Fahrenheit:
            unit = CleanText('//ul[@class="stats"]/li[8]/strong/text()')(self)
            unit = unit[-1]
            
            return Temperature(float(temp), unit)
        
    @method
    class iter_forecast(ListElement):
        
        """ The first temperature value on Accuweather forecasts depends on the moment of the day:
        for a city where the time is close to midnight, Accuweather displays both 'Early AM' and 'Today'.
        This may lead to duplicates for the obj_id since both elements correspond to the same date.
        In order to avoid duplicate issues, the iteration always starts at the second <li> of the HTML page."""
        
        item_xpath = '//div[@class="panel-body"]/div[@id="feed-tabs"]/ul/li[position()>1]'
        
        class item(ItemElement):
            klass = Forecast
            obj_id = CleanText('./div/h4/text()') #Date (example: 'Mar 27')
            obj_date = Format('%s  %s', CleanText('./div/h3/a/text()'), CleanText('./div/h4/text()')) #Day of the week (example: 'Sat') and Date (example: 'Mar 27')
            obj_text = Format('- %s', CleanText('.//span[@class="cond"]/text()')) #Weather prediction (example: 'Partly cloudy')
            
            def obj_low(self):
                temp = CleanText('.//span[@class="small-temp"]/text()')(self)
                # For some of the low temperature elements, the value ends with '°', for some others it ends with '°C' or '°F':
                if temp.endswith('C') or temp.endswith('F'):
                    temp = temp[1:-2]
                else:
                    temp=temp[1:-1]
                unit= CleanText('//span[@class="local-temp"]/text()')(self)
                unit = unit[-1]
                return Temperature(float(temp), unit)
    
            def obj_high(self):
                temp = CleanText('.//span[@class="large-temp"]/text()')(self)
                # Eliminating the '°' at the end:
                temp=temp[:-1]                
                unit= CleanText('//span[@class="local-temp"]/text()')(self)
                unit=unit[-1]
                return Temperature(float(temp), unit)

