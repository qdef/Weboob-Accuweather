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
from .browser import AccuweatherBrowser
from weboob.capabilities.weather import CapWeather, CityNotFound
from weboob.tools.backend import Module
from weboob.capabilities.base import find_object

__all__ = ['AccuweatherModule']

class AccuweatherModule(Module, CapWeather):
    NAME = 'accuweather'
    DESCRIPTION = u'accuweather website'
    MAINTAINER = u'Quentin Def'
    EMAIL = 'quentin.defenouillere@gmail.com'
    LICENSE = 'AGPLv3+'
    VERSION = '1.4'
    BROWSER = AccuweatherBrowser
    
    # Method to search for a city pattern:
    def iter_city_search(self, pattern):
        self.cities = list(self.browser.iter_city_search(pattern))
        # In case the city search returns no results:
        if not self.cities:
            raise CityNotFound('Sorry, no result matched your query.')
        return self.cities
    
    # Method to retrieve the weather data for one specific city: 
    def get_current(self, id):  
        return self.browser.get_current(id)

    # Method to get the weather forecast of the 4 next days for one specific city:
    def iter_forecast(self, id):  
        return self.browser.iter_forecast(id)
    

