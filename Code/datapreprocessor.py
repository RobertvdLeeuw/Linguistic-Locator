from collections import defaultdict
from pathlib import Path
import re

from customtools import CheckFile

import pandas as pd

SEPARATORS = defaultdict(lambda: r"\n\n")
SEPARATORS['An Essay Concerning Humane Understanding Vol II - Locke.txt'] = r"\n\n[0-9]\."  # Some sources have better results with custom separators.

# CHARSTOREMOVE = r"_|«|»|\"|\'"
# Only keeping letters, numbers and spaces. Also removing empty spaces before the first letter. Based on this filter:
# https://stackoverflow.com/questions/24676691/whats-a-good-regex-to-include-accented-characters-in-a-simple-way
CHARACTERFILTER = r"^( +)|[^-'\"a-zA-ZÀ-ÖØ-öø-ÿ0-9 ]"  # Could've perhaps used string.punctuation for this... Oh well.

splitText = dict()  # Title: [paragraph, paragraph, ...]


@CheckFile
def SplitText(file: Path) -> list:
	"""Splits the input text and returns a list of its paragraphs with all punctuation removed."""

	global SEPARATORS, CHARACTERFILTER

	with open(file.resolve(), 'r', encoding='utf-8') as textFile:  # UTF-8 saves the day, regarding 'nonconventional' characters from different languages.
		text = textFile.read().lower()

		segments = re.split(SEPARATORS[textFile.name], text)
		segments = [s.replace('\n', ' ') for s in segments]
		segments = [re.sub(CHARACTERFILTER, '', s) for s in segments]
	return segments


def LinkData(textData: dict, metaData: pd.DataFrame) -> pd.DataFrame:
	"""Merges the newly split paragraph data and metadata regarding the texts in order to output a dataframe of paragraphs, each labeled with its metadata."""

	linkedData = pd.DataFrame(columns=['Title', 'Text', 'Language', 'Year', 'Longitude', 'Latitude'])
	for title, textList in textData.items():
		title, language, year, longitude, latitude = metaData.loc[metaData['Title'] == title].squeeze().tolist()  # Not using the title.

		for paragraph in textList:
			linkedData.loc[len(linkedData.index)] = [title, paragraph, language, year, longitude, latitude]
	return linkedData


def GetData(textFiles: list, csv: pd.DataFrame):
	"""Retrieves the text data and it's metadata in order to return a merged cleaned dataset of paragraphs and addditional information."""

	global splitText

	for file in textFiles:
		data = SplitText(file)
		data.sort(key=len)

		data = list(filter(lambda x: len(x.strip()) > 500, data))  # Elaborate on size <--> amount balance.

		splitText[file.name] = data
	data = LinkData(splitText, csv)

	return data
