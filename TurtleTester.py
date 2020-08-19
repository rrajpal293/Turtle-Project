import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from numpy import log, exp, sqrt
from scipy.stats import norm

_data = pd.read_excel('USDJPYDailyPrices.xlsx', sheet_name='Sheet1')  
ts = TurtleSystem(_data)
 
# ts.populateRollingHighsAndLows()
# ts.populateTR()
# ts.populateN()
# hd = HistData(_data, 'JPYUSD')
# print (hd)
#tr = TurtleSystem(20)
#ts.setData(hd)
#dff = ts.getData()
