TurtleSystem.py
Details
Activity
Sharing Info
Not shared
General Info
Type
Text
Size
10 KB (10,308 bytes)
Storage used
65 KB (66,866 bytes)
Location
Crescent
Owner
me
Modified
10:44 AM by me
Opened
10:44 AM by me
Created
Aug 18, 2020 with Google Drive Web
Description
Add a description
Download permissions
Viewers can download

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy import log, exp, sqrt
from scipy.stats import norm

# This class implements the Turle System
# Since there is no intraday data, the rules cannot be followed exactly as descriobed in the document
# The code below implements the System without the  Whipsaw rule and makes the following simplifying assumptiuons;
# 1. all trading is done at the Close even though according to the rules trades should
# be done at the open if the breakout or stop loss/ exit rules are triggered  at the Open price
# 2. Additional units are added at the close even though according to the rules additional units should be 
# added as and when different higher (or lower) levels are hit

class TurtleSystem():  
    # Inputs & intermediate values
    _data = None # This contains the raw historical data as wellas  processed data such as rolling highs, lows, N, TR,  etc
    _breakoutLength1 = None # the rolling window length to calculate System 1 breakout signal
    _breakoutLength2 = None # the rolling window length to calculate System 2 breakout signal
    _exitLength1 = None # the rolling window length to calculate System 1 exit signal
    _exitLength2 = None # the rolling window length to calculate System 2 exit signal
    _dxSimulationStart = None # start date for simulation
    _dxSimulationEnd = None # end date for simulation
    _currentSignal = 0 # current value of Signal
    _currentEntryPoint = None # updated Entry Point
    _currentExitPoint = None # updated Exit Point
    _currentBODUnits = 0 # Number of Position Units at the start of the day
    _currentEODUnits = 0 # Number of position units at the end of the day
    _currentN = None # current value of N
    _currentTR = None  # current value of TR

    # Outputs
    _results = None # This is the dataframe containing the desired output infiormation: Signal, Entry/Exit Level, Position Units
    def __init__(self, nBreakout1 = 20, nBreakout2 = 55, nExit1 = 10, nExit2 = 20): #initialized with System 1 & SYstem2 default parameters
        self._breakoutLength1 = nBreakout1
        self._breakoutLength2 = nBreakout2
        self._exitLength1 = nExit1
        self._exitLength2 = nExit2
        _results = SimResults()


    def getData(self):
        return self._data

    def setData(self, dfhistData) #populate _data with the raw data
        self._data = dfHistData
        self.processRawData()

    def getResults(self):
        return self._results

    def processRaWData() 
        # create new columns based on existing columns
        self._data['PrevClose'] = self._data['Close'].shift(1)
        # create a placeholder column for True Range
        self._data['TR'] = np.ones((_numdates,1)) * np.nan
        # create a placeholder column for N
        self._data['N'] = np.ones((_numdates,1)) * np.nan
        self.populateRollingHighsAndLows() # add columns in _data for rollimng highs and lows
        self.populateTR() # populate TR column in _data
        self.populateN() # populate N column in _data


    def populateRollingHighsAndLows(self):
        self._data['Entry1DayHigh'] = self._data['PrevClose'].rolling(window=self._breakoutLength1).max()
        self._data['Entry1Daylow'] = self._data['PrevClose'].rolling(window=self._breakoutLength1).min()
        #self._data['Entry2DayHigh'] = self._data['PrevClose'].rolling(window=self._breakoutLength2).max()
        #self._data['Entry2Daylow'] = self._data['PrevClose'].rolling(window=self._breakoutLength2).min()
        self._data['Exit1DayHigh'] = self._data['Close'].rolling(window=self._exitLength1).max()
        self._data['Exit1Daylow'] = self._data['Close'].rolling(window=self._exitLength1).min()
        #self._data['Exit2DayHigh'] = self._data['Close'].rolling(window=self._exitLength2).max()
        #self._data['Exit2Daylow'] = self._data['Close'].rolling(window=self._exitLength2).min()


    def populateTR(self): # TR = max(High - Low, High - PDC, PDC - Low)
        for ind in self._data.index:
            if ind > 0:
                self._data['TR'][ind] = max(self._data['High'][ind-1] - self._data['Low'][ind-1], self._data['High'][ind-1] - self._data['PrevClose'][ind], self._data['PrevClose'][ind] - self._data['Low'][ind-1])
            else;
                self._data['TR'][ind] = max(self._data['High'][ind] - self._data['Low'][ind], self._data['High'][ind] - self._data['PrevClose'][ind], self._data['PrevClose'][ind] - self._data['Low'][ind])

    def populateN(self): # N is the 20-day exponential moving average of TR
        self._data['N'][self._breakoutLength1-1] = self._data['TR'][:self._breakoutLength1-1].mean() #take simple average of the first 20 values of TR
        for ind in self._data.index:
            if ind >= self._breakoutLength1:
                self._data['N'][ind] = 0.95 * self._data['N'][ind-1] + 0.05 * self._data['TR'][ind]

    def calculateSimDates(self): #calculates the start andend date for thesimulation
        self._dxSimulationStart = self._data['Date'].iloc[_breakoutLength1 + 1]
        self._dxSimulationEnd = self._data['Date'].iloc[self._data.NumDates()]

    def SimulateOneDay(self, dt, nSimDay): # simulates one day or trading
        if self._data['Date'].loc[dt] >= self._dxSimulationStart & self._data['Date'].loc[dt] <= self._dxSimulationEnd:
            self._currentEODUnits = self._currentBODUnits
            self._currentSignal = self.calculateSignal(self, dt, nSimDay)
            self._currentEntryPoint = self.calculateEntryPoint(self, _currentSignal, dt, nSimDay)
            self._currentExitPoint = self.calculateExitPoint(self, _currentSignal, dt)
            self._results.Append(dt, _currentSignal, _currentEntryPoint, _currentExitPoint, _currentBODUnits, _currentEODUnits)
            self._currentBODUnits = self._currentEODUnits

    def Simulate(self): #simulates trading between simulation start date and simulation end date
        self.calculateSimDates()
        numSimDays = 0
        for dt in _data['Date']:
            self.SimulateOneDay(dt, numSimDays)
            numSimDays++
        

    def calculateSignal(self, dt, nSimDay): #1 = buy, -1 = sell short, 0.5/-0.5 = exit because exit rule was hit, 0.25/-0.25 = exit because rolling stop loss was hit, 0 otherwise
        if self._data['Entry1DayHigh'].loc[dt] < self._data['High'].loc[dt]:
            return 1
        if self._data['Entry1DayLow'].loc[dt] > self._data['Low'].loc[dt]:
            return -1
        if nSimDays > 0
            if ((self._data['Exit1DayHigh'].loc[dt] < self._data['High'].loc[dt]) and (_BODUnits < 0)):
                return 0.5
            if ((self._data['Exit1DayLow'].loc[dt] > self._data['Low'].loc[dt]) and (_BODUnits > 0)):
                return -0.5
            if ((self._data['Entry1DayHigh'].loc[dt] + 2 * self._data['N'].iloc[_breakoutLength1+nSimDay] < self._data['High'].loc[dt]) and (_BODUnits < 0)):
                return 0.25
            if ((self._data['Entry1DayHigh'].loc[dt] - 2 * self._data['N'].iloc[_breakoutLength1+nSimDay] > self._data['Low'].loc[dt]) and (_BODUnits > 0)):
                return -0.25
        return 0   


    def calculateEntryPoint(self, Signal, dt, nSimDay): # calculates the entry point for a new unit(s) and update thenumber of units
        if abs(Signal) < 1 and abs(Signal) > 0: # is Signal was an exit signal, then there is no entry point
            return None
        if ((Signal == 1) and (self._currentBODUnits <= 0)): # if signal is a buy and ssytem was not already long then entry point s today's close
            return max(self._data['Entry1DayHigh'].loc[dt], self._data['Close'].loc[dt])
        if ((Signal == -1) and (self._currentBODUnits >= 0)): # if signal is a sell and ssytem was not already short then entry point s today's close
            return min(self._data['Entry1DayLow'].loc[dt], self._data['Close'].loc[dt])
        if ((abs(Signal) == 1) and (self._currentBODUnits == 4)): # if we already have 4 units, then we don't add to the position
            return self._results['Entry Level'].iloc[nSimDay-1]   
        # If there is already a long position that is being aaded to then calculate additional number of units, 
        # which depends on how much the price moved from entry level divided by 0.5 * N
        if ((Signal >= 0) and (self._currentBODUnits > 0)): 
            additionalUnits = min(4-self._currentBODUnits, (self._data['High'].loc[dt] - self._results['Entry Level'].iloc[nSimDay-1])/(0.5 * self._data['N'].loc[dt]))
            self._currentEODUnits = self._currentBODUnits + additionalUnits
            if additionalUnits == 0:
                return self._results['Entry Level'].iloc[nSimDay-1]   
            else:
                return = (self._results['Entry Level'].iloc[nSimDay-1] * self._currentBODUnits + self._data['Close'].loc[dt] * additionalUnits)/(self._currentBODUnits + additionalUnits)
        # If there is already a short position that is being aaded to then calculate additional number of units, 
        # which depends on how much the price moved from entry level divided by 0.5 * N
        if ((Signal <= 0) and (self._currentBODUnits < 0)):
            additionalUnits = min(-4-self._currentBODUnits, (self._data['Low'].loc[dt] - self._results['Entry Level'].iloc[nSimDay-1])/(0.5 * self._data['N'].loc[dt]))
            self._currentEODUnits = self._currentBODUnits + additionalUnits
            if additionalUnits == 0:
                return self._results['Entry Level'].iloc[nSimDay-1]   
            else:
                return = (self._results['Entry Level'].iloc[nSimDay-1] * self._currentBODUnits + self._data['Close'].loc[dt] * additionalUnits)/(self._currentBODUnits + additionalUnits) 
        return None
           
    def calculateExitPoint(self, Signal, dt):  # calculates the exit point
        if (abs(Signal) > 0 and abs(Signal) < 1):
            self._currentEODUnits = 0
            return self._data['Close'].loc[dt]
        if ((Signal == 1) and (self._currentBODUnits < 0)):
            self._currentEODUnits = 1
            return self._data['Close'].loc[dt]
        if ((Signal == -1) and (self._currentBODUnits > 0)):
            self._currentEODUnits = -1
            return self._data['Close'].loc[dt]
        return None
