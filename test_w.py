#
import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



dataset = pd.read_csv('PANDAS_CLEAN_DATA.csv', sep='\t', encoding='utf-8')


scams = dataset[dataset.price <700]
scams.to_csv('TEST.csv', sep='\t', encoding='utf-8', index=True)
print(scams.info())
#print(scams.head(10))