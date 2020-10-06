import pandas as pd
import numpy as np

data = pd.read_excel('defaulter_list.xlsx')
df = pd.DataFrame(data, rows=['51001'])
print(df)