from collections import defaultdict
from os import listdir
from pathlib import Path

from customtools import CheckFile

import re
import numpy as np
import pandas as pd

SEPARATORS = defaultdict(lambda: r"\n\n")
SEPARATORS['An Essay Concerning Humane Understanding Vol II - Locke.txt'] = r"\n\n[0-9]\."  # Some sources have better results with custom separators.

files = [Path(f'D:\\Documents\\Fontys\\S4\\Language\\Data\\Raw\\{file}') for file in listdir('D:\\Documents\\Fontys\\S4\\Language\\Data\\Raw')]
splitText = dict()  # Title: [paragraph, paragraph, ...]


@CheckFile
def GetSplitText(file: Path) -> list:
	global SEPARATORS

	with open(file.resolve(), 'r', encoding='utf-8') as textFile:
		text = textFile.read()

		segments = re.split(SEPARATORS[textFile.name], text)
	return segments


def LinkData(textData: dict, metaData: pd.DataFrame) -> pd.DataFrame:
	linkedData = pd.DataFrame(columns=['Title', 'Text', 'Language', 'Year', 'Longitude', 'Latitude'])
	for title, textList in textData.items():
		title, language, year, longitude, latitude = metaData.loc[metaData['Title'] == title].squeeze().tolist()  # Not using the title.

		for paragraph in textList:
			linkedData.loc[len(linkedData.index)] = [title, paragraph, language, year, longitude, latitude]
	return linkedData


if __name__ == '__main__':
	for file in files:
		data = GetSplitText(file)
		data.sort(key=len)

		data = list(filter(lambda x: len(x.strip()) > 500, data))  # Elaborate on size <--> amount balance.

		splitText[file.name] = data
	data = LinkData(splitText, pd.read_csv('D:\Documents\Fontys\S4\Language\Data\Done\Metadata.csv', encoding='unicode_escape'))

	# data.to_csv('D:\\Documents\\Fontys\\S4\\Language\\Data\\Done\\Data.csv', index=False, encoding='utf-8')

	'''for key, val in splitText.items():
		length = len(val)
		print(len(val))
		print(key, val[0])
		
	df = pd.DataFrame.from_dict(splitText, orient='index')
	df = df.transpose()
	df.to_csv('D:\\Documents\\Fontys\\S4\\Language\\Code\\out.csv')'''
