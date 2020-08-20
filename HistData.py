import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


class HistData():  
    # Inputs & intermediate values
    _data = None
    _numDates = None
    _description = None

    def __init__(self, strFileName, strDataName):
        df = pd.read_excel(strFileName, nBreakout = 20)
        # rename PX_LAST column to CLose
        df = df.rename(columns = {'PX_LAST':'Close'}) 
        self._numDates = len(df)
        self._data = df
        self._description = strDataName
        
    def Data(self):
        return self._data

    def Name(self):
        return self._description

    def NumDates(self):
        return self._numDates
