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
from weboob.tools.test import BackendTest


class AccuweatherTest(BackendTest):
    MODULE = 'accuweather'

    def test_accuweather(self):
        
        # Checking that a unique city search actually returns a unique search result:
        k = list(self.backend.iter_city_search('rognonas'))
        self.assertTrue(len(k) == 1)
        
        # Checking that a 'paris' search actually returns several results:
        l = list(self.backend.iter_city_search('paris'))
        self.assertTrue(len(l) > 0)
        
        """Testing the 'current' method"""
        city = l[0]
        current = self.backend.get_current(city.id)
        
        # Verifying the unit possibilities:
        self.assertTrue(current.temp.unit in ['C', 'F'])
        
        # Checking that the paris temperature value is within the usual temperature range (-20 to 50°C):
        if current.temp.unit == 'C':
            self.assertTrue(current.temp.value > -20 and current.temp.value < 50)
        # In case the temperature is in Fahrenheit:
        elif current.temp.unit == 'F':
            self.assertTrue(current.temp.value > -4 and current.temp.value < 130)
        
        """Testing the 'forecast' method"""
        forecasts = list(self.backend.iter_forecast(city.id))
        
        # Verifying that the forecast list contains the 4 next days:
        self.assertTrue(len(forecasts) == 4)
        
        # Verifying the units for each of the forecast days (for low and high temperatures):
        for units in forecasts:
            self.assertTrue(units.high.unit in ['C', 'F'])
            self.assertTrue(units.low.unit in ['C', 'F'])
