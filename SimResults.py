import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import SimResults
import HistData

class SimResults():  
    # Inputs & intermediate values
    _data = None

    def __init__(self):
    	# create a blank simulation results dataframe
        df = pd.DataFrame(columns=['Date', 'Signal', 'Entry Level', 'Exit Level','BOD Units', 'EOD Units', 'DailyReturn'])
        self._data = df
        
    def Data(self):
        return self._data

    def Append(self, dt, Signal, EntryLevel, ExitLevel, BODUnits, EODUnits, Strat_Return):
    	#if sum(self._data['Date'] == dt) == 0: # if date does not exist then append otherise update
        self._data = self._data.append({'Date' : dt, 'Signal': Signal, 'Entry Level' : EntryLevel, 'Exit Level' : ExitLevel, 'BOD Units' : BODUnits, 'EOD Units' : EODUnits, 'DailyReturn': Strat_Return}, ignore_index = True)
    	#else:
    	#	self.Update(dt, 'Signal',Signal)
    	#	self.Update(dt, 'Entry Level', EntryLevel)
    	#	self.Update(dt, 'Exit Level', ExitLevel)
    	#	self.Update(dt, 'BOD Units', BODUnits)
    	#	self.Update(dt, 'EOD Units', EODUnits)

    def Update(self, dt, strField, value):
        if sum(_data['Date'] == dt) == 1: # only update if date already exists, othwrwise append
        	df.loc[df['Date'] == dt, strField] = value
        else:
        	self._data.append({'data' : dt, strField : value})
    def DrawPNL(self):
        self._data[['DailyReturn']].cumsum().plot()
    def TotalReturn(self):
        return self._data[['DailyReturn']].sum().apply(np.exp)
