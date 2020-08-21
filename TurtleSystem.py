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
    _data = None # This contains the raw historical data as well as processed data such as rolling highs, lows, N, TR,  etc
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
    _arrayN = None
    _resultsdf = None

    # Outputs
    _results = None # This is the dataframe containing the desired output infiormation: Signal, Entry/Exit Level, Position Units
    def __init__(self, nBreakout1 = 20, nBreakout2 = 55, nExit1 = 10, nExit2 = 20): #initialized with System 1 & SYstem2 default parameters
        self._breakoutLength1 = nBreakout1
        self._breakoutLength2 = nBreakout2
        self._exitLength1 = nExit1
        self._exitLength2 = nExit2
        self._results = SimResults()
        self._resultsdf = self._results.Data()
        #self._results = sr.Data()

    def getData(self):
        return self._data

    def setData(self, dfHistData): #populate _data with the raw data
        self._data = dfHistData.Data()
        self.processRawData()
        self._arrayN = self._data['N'].values

    def getResults(self):
        return self._results

    def processRawData(self): 
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
        self._data['Entry1DayLow'] = self._data['PrevClose'].rolling(window=self._breakoutLength1).min()
        #self._data['Entry2DayHigh'] = self._data['PrevClose'].rolling(window=self._breakoutLength2).max()
        #self._data['Entry2Daylow'] = self._data['PrevClose'].rolling(window=self._breakoutLength2).min()
        self._data['Exit1DayHigh'] = self._data['Close'].rolling(window=self._exitLength1).max()
        self._data['Exit1DayLow'] = self._data['Close'].rolling(window=self._exitLength1).min()
        #self._data['Exit2DayHigh'] = self._data['Close'].rolling(window=self._exitLength2).max()
        #self._data['Exit2Daylow'] = self._data['Close'].rolling(window=self._exitLength2).min()


    def populateTR(self): # TR = max(High - Low, High - PDC, PDC - Low)
        for ind in self._data.index:
            if ind > 0:
                self._data['TR'][ind] = max(self._data['High'][ind-1] - self._data['Low'][ind-1], self._data['High'][ind-1] - self._data['PrevClose'][ind], self._data['PrevClose'][ind] - self._data['Low'][ind-1])
            else:
                self._data['TR'][ind] = max(self._data['High'][ind] - self._data['Low'][ind], self._data['High'][ind] - self._data['PrevClose'][ind], self._data['PrevClose'][ind] - self._data['Low'][ind])

    def populateN(self): # N is the 20-day exponential moving average of TR
        self._data['N'][self._breakoutLength1-1] = self._data['TR'][:self._breakoutLength1-1].mean() #take simple average of the first 20 values of TR
        for ind in self._data.index:
            if ind >= self._breakoutLength1:
                self._data['N'][ind] = 0.95 * self._data['N'][ind-1] + 0.05 * self._data['TR'][ind]

    def calculateSimDates(self): #calculates the start and end date for the simulation
        self._dxSimulationStart = self._data['Date'].iloc[self._breakoutLength1 + 1]
        self._dxSimulationEnd = self._data['Date'].iloc[len(self._data)-1]
        # self._data.set_index(['Date'], inplace = True)

    def SimulateOneDay(self, dt, nSimDay): # simulates one day or trading
        #if (self._data['Date'].iloc[nSimDay + self._breakoutLength1-1] >= self._dxSimulationStart) and (self._data['Date'].iloc[nSimDay + self._breakoutLength1-1] <= self._dxSimulationEnd):
        self._resultsdf = self._results.Data()
        print(len(self._resultsdf))
        self._currentEODUnits = self._currentBODUnits
        self._currentSignal = self.calculateSignal(dt, nSimDay)
        self._currentEntryPoint = self.calculateEntryPoint(self._currentSignal, dt, nSimDay)
        self._currentExitPoint = self.calculateExitPoint(self._currentSignal, dt, nSimDay)
        print([self._currentSignal, self._currentEntryPoint, self._currentExitPoint, self._currentBODUnits, self._currentEODUnits])
        self._results.Append(dt, self._currentSignal, self._currentEntryPoint, self._currentExitPoint, self._currentBODUnits, self._currentEODUnits)
        self._currentBODUnits = self._currentEODUnits

    def Simulate(self): #simulates trading between simulation start date and simulation end date
        self.calculateSimDates()
        numSimDays = 0
        allDates = self._data['Date'][self._breakoutLength1-1:]
        # self._data.set_index(['Date'], inplace = True)
        #print(self._data)
        for dt in allDates:
            print(dt)
            self.SimulateOneDay(dt, numSimDays)
            numSimDays = numSimDays + 1
        # self._data.reset_index(['Date'], inplace = False)

    def calculateSignal(self, dtt, nSimDay): #1 = buy, -1 = sell short, 0.5/-0.5 = exit because exit rule was hit, 0.25/-0.25 = exit because rolling stop loss was hit, 0 otherwise
        dt = self._breakoutLength1+nSimDay-1
        if self._data['Entry1DayHigh'].iloc[dt] < self._data['High'].iloc[dt]:
            return 1
        if self._data['Entry1DayLow'].iloc[dt] > self._data['Low'].iloc[dt]:
            return -1
        if nSimDay > 0:
            if ((self._data['Exit1DayHigh'].iloc[dt] < self._data['High'].iloc[dt]) and (self._currentBODUnits < 0)):
                return 0.5
            if ((self._data['Exit1DayLow'].iloc[dt] > self._data['Low'].iloc[dt]) and (self._currentBODUnits > 0)):
                return -0.5
            if ((self._data['Entry1DayHigh'].iloc[dt] + 2 * self._arrayN[dt] < self._data['High'].iloc[dt]) and (self._currentBODUnits < 0)):
                return 0.25
            if ((self._data['Entry1DayHigh'].iloc[dt] - 2 * self._arrayN[dt] > self._data['Low'].iloc[dt]) and (self._currentBODUnits > 0)):
                return -0.25
        return 0   


    def calculateEntryPoint(self, Signal, dtt, nSimDay): # calculates the entry point for a new unit(s) and update thenumber of units
        dt = self._breakoutLength1+nSimDay-1
        print([nSimDay, dt])
        if abs(Signal) < 1 and abs(Signal) > 0: # is Signal was an exit signal, then there is no entry point
            return None
        if ((Signal == 1) and (self._currentBODUnits <= 0)): # if signal is a buy and ssytem was not already long then entry point s today's close
            self._currentEODUnits = 1
            return max(self._data['Entry1DayHigh'].iloc[dt], self._data['Close'].iloc[dt])
        if ((Signal == -1) and (self._currentBODUnits >= 0)): # if signal is a sell and ssytem was not already short then entry point s today's close
            self._currentEODUnits = -1
            return min(self._data['Entry1DayLow'].iloc[dt], self._data['Close'].iloc[dt])
        if ((abs(Signal) == 1) and (self._currentBODUnits == 4)): # if we already have 4 units, then we don't add to the position
            return self._resultsdf['Entry Level'].iloc[nSimDay-1]   
        # If there is already a long position that is being aaded to then calculate additional number of units, 
        # which depends on how much the price moved from entry level divided by 0.5 * N
        if ((Signal >= 0) and (self._currentBODUnits > 0)): 
            additionalUnits = min(4-self._currentBODUnits, (self._data['High'].iloc[dt] - self._resultsdf['Entry Level'].iloc[nSimDay-1])/(0.5 * self._data['N'].iloc[dt]))
            self._currentEODUnits = self._currentBODUnits + additionalUnits
            if additionalUnits == 0:
                return self._resultsdf['Entry Level'].iloc[nSimDay-1]   
            else:
                return (self._resultsdf['Entry Level'].iloc[nSimDay-1] * self._currentBODUnits + self._data['Close'].iloc[dt] * additionalUnits)/(self._currentBODUnits + additionalUnits)
        # If there is already a short position that is being aaded to then calculate additional number of units, 
        # which depends on how much the price moved from entry level divided by 0.5 * N
        if ((Signal <= 0) and (self._currentBODUnits < 0)):
            additionalUnits = min(-4-self._currentBODUnits, (self._data['Low'].iloc[dt] - self._resultsdf['Entry Level'].iloc[nSimDay-1])/(0.5 * self._data['N'].iloc[dt]))
            self._currentEODUnits = self._currentBODUnits + additionalUnits
            if additionalUnits == 0:
                return self._resultsdf['Entry Level'].iloc[nSimDay-1]   
            else:
                return (self._resultsdf['Entry Level'].iloc[nSimDay-1] * self._currentBODUnits + self._data['Close'].iloc[dt] * additionalUnits)/(self._currentBODUnits + additionalUnits) 
        return None
           
    def calculateExitPoint(self, Signal, dt, nSimDay):  # calculates the exit point
        dt = self._breakoutLength1+nSimDay-1
        if (abs(Signal) > 0 and abs(Signal) < 1):
            self._currentEODUnits = 0
            return self._data['Close'].iloc[dt]
        if ((Signal == 1) and (self._currentBODUnits < 0)):
            self._currentEODUnits = 1
            return self._data['Close'].iloc[dt]
        if ((Signal == -1) and (self._currentBODUnits > 0)):
            self._currentEODUnits = -1
            return self._data['Close'].iloc[dt]
        return None
