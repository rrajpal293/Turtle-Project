import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy import log, exp, sqrt
from scipy.stats import norm


class TurtleSystem():  
    # Inputs & intermediate values
    _data = None
    _breakoutLength1 = None
    _breakoutLength2 = None
    _exitLength1 = None
    _exitLength2 = None
    _dxSimulationStart = None
    _dxSimulationEnd = None
    _currentSignal = None
    _currentEntryPoint = None
    _currentExitPoint = None
    _currentNumUnits = None

    # Outputs
    _results = None

    def __init__(self, nBreakout1 = 20, nBreakout2 = 55, nExit1 = 10, nExit2 = 20):
        self._breakoutLength1 = nBreakout1
        self._breakoutLength2 = nBreakout2
        self._exitLength1 = nExit1
        self._exitLength2 = nExit2
        #_results = 


    def getData(self):
        return self._data

    def setData(self, dfHistData):
        self._data = dfHistData
        self.processRawData()

    def getResults(self):
        return self._results

    def processRaWData():
        # create new columns based on existing columns
        self._data['PrevClose'] = self._data['Close'].shift(1)
        # create a placeholder column for True Range
        self._data['TR'] = np.ones((_numdates,1)) * np.nan
        # create a placeholder column for N
        self._data['N'] = np.ones((_numdates,1)) * np.nan
        self.populateRollingHighsAndLows()
        self.populateTR()
        self.populateN()


    def populateRollingHighsAndLows(self):
        self._data['Entry1DayHigh'] = self._data['PrevClose'].rolling(window=self._breakoutLength1).max()
        self._data['Entry1Daylow'] = self._data['PrevClose'].rolling(window=self._breakoutLength1).min()
        self._data['Entry2DayHigh'] = self._data['PrevClose'].rolling(window=self._breakoutLength2).max()
        self._data['Entry2Daylow'] = self._data['PrevClose'].rolling(window=self._breakoutLength2).min()
        self._data['Exit1DayHigh'] = self._data['Close'].rolling(window=self._exitLength1).max()
        self._data['Exit1Daylow'] = self._data['Close'].rolling(window=self._exitLength1).min()
        self._data['Exit2DayHigh'] = self._data['Close'].rolling(window=self._exitLength2).max()
        self._data['Exit2Daylow'] = self._data['Close'].rolling(window=self._exitLength2).min()


    def populateTR(self):
        for ind in self._data.index:
            self._data['TR'][ind] = max(self._data['High'][ind] - self._data['Low'][ind], self._data['High'][ind] - self._data['PrevClose'][ind], self._data['PrevClose'][ind] - self._data['Low'][ind])

    def populateN(self):
        self._data['N'][self._breakoutLength-1] = self._data['TR'][:self._breakoutLength-1].mean() #take simple average of the first 20 values of TR
        for ind in self._data.index:
            if ind >= self._breakoutLength:
                self._data['N'][ind] = 0.95 * self._data['N'][ind-1] + 0.05 * self._data['TR'][ind]

    def calculateSimDates(self):
        self._dxSimulationStart = self._data['Date'].iloc[_breakoutLength2 + 1]
        self._dxSimulationEnd = self._data['Date'].iloc[self._data.NumDates()]

    def SimulateOneDay(self, dt):
        if self._data['Date'].loc[dt] >= self._dxSimulationStart & self._data['Date'].loc[dt] <= self._dxSimulationEnd:
            Signal = self.calculateSignal(self, dt)
            EntryPoint = self.calculateEntryPoint(self, dt)
            ExitPoint = self.calculateExitPoint(self, dt)
            NumUnits = self.calculateNumUnits(self, dt)
            _results.Append(dt, Signal, EntryPoint, ExitPoint, NumUnits)

    def Simulate(self):
        self.calculateSimDates()
        for dt in _data['Date']:
            self.SimulateOneDay(dt) 

    #def calculateSignal(self, dt):
    
    #def calculateEntryPoint(self, dt):

    #def calculateExitPoint(self, dt):

    #def calculateNumUnits(self, dt):
