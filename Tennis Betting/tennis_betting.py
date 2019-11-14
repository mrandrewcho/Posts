#%%
import pandas as pd
import numpy as np 
import glob, os

#%%
data = pd.read_excel('2001.xls')

#%%
data

#%%
#os.chdir('Tennis Betting')
data = pd.DataFrame()
for file in glob.glob("*.xls*"):
    data = data.append(pd.read_excel(file))
#%%
data

#%%
data.describe()

#%%
#OKOKOK donezo