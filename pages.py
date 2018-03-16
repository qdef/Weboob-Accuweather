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
            klass = City
            obj_id = Dict('Key')
            obj_name = Format(u'%s - %s, %s', Dict('LocalizedName'), Dict['AdministrativeArea']['LocalizedName'], Dict['Country']['LocalizedName'])

class WeatherPage(HTMLPage):
    @method
    class get_current(ItemElement):
        klass = Current
        #obj_id = Env('city_id')
        obj_date = date.today()
        
        obj_text = Format(' %s - Wind speed: %s - Humidity: %s - Pressure: %s - UV index: %s - Cloud cover: %s.',
                          CleanText('//div[@id="details"]//span[@class="cond"]/text()'), #Weather condition
                          CleanText('//ul[@class="stats"]/li[2]/strong/text()'), #Wind speed
                          CleanText('//ul[@class="stats"]/li[3]/strong/text()'), #Humidity
                          CleanText('//ul[@class="stats"]/li[4]/strong/text()'), #Pressure
                          CleanText('//ul[@class="stats"]/li[5]/strong/text()'), #UV index
                          CleanText('//ul[@class="stats"]/li[6]/strong/text()')) #Cloud cover

        def obj_temp(self):
            temp = CleanText('//div[@id="details"]//span[@class="large-temp"]/text()')(self)
            temp=temp[:-1]
            temp = CleanDecimal(temp)(self)
            unit = CleanText('//ul[@class="stats"]/li[8]/strong/text()')(self)
            unit = unit[-1]
            return Temperature(float(temp), unit)
        
    @method
    class iter_forecast(ListElement):
        item_xpath = '//div[@class="panel-body"]/div[@id="feed-tabs"]/ul/li[position()>1]'
        
        class item(ItemElement):
            klass = Forecast
            obj_id = CleanText('.//h3/a/text()')
            obj_date = Format('%s  %s', CleanText('./div/h3/a/text()'), CleanText('./div/h4/text()'))
            obj_text = Format('- %s', CleanText('.//span[@class="cond"]/text()'))
            
            def obj_low(self):
                temp = CleanText('.//span[@class="small-temp"]/text()')(self)
                if temp.endswith('C') or temp.endswith('F'):
                    temp = temp[1:-2]
                else:
                    temp=temp[1:-1]
                unit= CleanText('//span[@class="local-temp"]/text()')(self)
                unit=unit[-1]
                return Temperature(float(temp), unit)
    
            def obj_high(self):
                temp = CleanText('.//span[@class="large-temp"]/text()')(self)
                temp=temp[:-1]                
                unit= CleanText('//span[@class="local-temp"]/text()')(self)
                unit=unit[-1]                
                return Temperature(float(temp), unit)

