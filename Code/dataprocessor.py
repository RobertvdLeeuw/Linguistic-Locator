from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import numpy as np
import pandas as pd


class DataSegment:
	x: list
	y: list


# Might merge the methods below into 1 someday. Decorator + match case (goes against idea of generality).

def SettingsManager(function):
	def wrapper(*args, **kwargs):

		output = function(*args, **kwargs)

		return output

	return wrapper


@SettingsManager
def PredictLanguage(train: DataSegment, test: DataSegment):  # Classification, not clustering
	pass


@SettingsManager
def PredictTime(train: DataSegment, test: DataSegment):  # Regression
	pass


@SettingsManager
def PredictLocation(train: DataSegment, test: DataSegment):  # Multi-output regression
	pass
