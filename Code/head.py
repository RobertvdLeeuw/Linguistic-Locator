from datapreprocessor import GetData

from os import listdir
from pathlib import Path

import pandas as pd


files = [Path(f'D:\\Documents\\Fontys\\S4\\Language\\Data\\Raw\\{file}') for file in listdir('D:\\Documents\\Fontys\\S4\\Language\\Data\\Raw')]

if __name__ == '__main__':
	data = GetData(files, pd.read_csv('D:\\Documents\\Fontys\\S4\\Language\\Data\\Done\\Metadata.csv', encoding='unicode_escape'))
	data.to_csv('D:\\Documents\\Fontys\\S4\\Language\\Data\\Done\\Data.csv', index=False, encoding='utf-8')
