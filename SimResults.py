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
        df = pd.DataFrame(columns=['Date', 'Signal', 'Entry Level', 'Exit Level','BOD Units', 'EOD Units'])
        self._data = df
        
    def Data(self):
        return self._data

    def Append(self, dt, Signal, EntryLevel, ExitLevel, Units):
    	if sum(self._data['Date'] == dt) == 0: # if date does not exist then append otherise update
    		self._data.append({'data' : dt, 'Signal': Signal, 'Entry Level' : EntryLevel, 'Exit Level' : ExitLevel, 'BOD Units' : BODUnits, 'EODUnits' : EODUnits})
    	else:
    		self.Update(dt, 'Signal',Signal)
    		self.Update(dt, 'Entry Level', EntryLevel)
    		self.Update(dt, 'Exit Level', ExitLevel)
    		self.Update(dt, 'BOD Units', Units)
    		self.Update(dt, 'EOD Units', Units)

    def Update(self, dt, strField, value):
        if sum(_data['Date'] == dt) == 1: # only update if date already exists, othwrwise append
        	df.loc[df['Date'] == dt, strField] = value
        else:
        	self._data.append({'data' : dt, strField : value})
 
