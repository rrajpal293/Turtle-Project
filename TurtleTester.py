import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from numpy import log, exp, sqrt
from scipy.stats import norm
from Option_Vals import Option_Vals

url = '/Users/rohunrajpal/Python Code/FX Options/USDJPY Daily Prices.xlsx'
hd = HistData(url, 'JPYUSD')
ts = TurtleSystem(20)
ts.setData(hd)
ts.Simulate()
results = ts.getResults()
print(results.Data())
results.Data().to_csv('turtle_simulation.csv')
results.DrawPNL()
