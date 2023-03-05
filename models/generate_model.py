import logging
import pickle
from math import sqrt

import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler


class HousingPricesDataPreprocessor:
	yearly_data = None
	monthly_data = None

	def __init__(self, yearly_data_path, monthly_data_path):
		self.yearly_data = pd.read_csv(yearly_data_path)
		self.monthly_data = pd.read_csv(monthly_data_path)		

	def preprocess(self, encoder=LabelEncoder()):
		# Convert date column type to datetime
		self.yearly_data['date'] = pd.to_datetime(self.yearly_data['date'])
		self.monthly_data['date'] = pd.to_datetime(self.monthly_data['date'])

		# 2) For simplicity, use only some features and drop the rest
		relevant_yearly_features = [
			'area',
			'date',
			'median_salary',
			'population_size'
		]
		relevant_monthly_features = [
			'area', 
			'date',
			'average_price',
			'houses_sold'
		]
		self.yearly_data = self.yearly_data[relevant_yearly_features]
		self.monthly_data = self.monthly_data[relevant_monthly_features]

		# Get the year from the date
		self.yearly_data = (
			self.yearly_data.dropna(
				subset=['median_salary', 'population_size'])
		)
		self.monthly_data = self.monthly_data.dropna(subset=['houses_sold'])
		self.yearly_data['year'] = (
			pd.DatetimeIndex(self.yearly_data['date'])
			.year
		)
		self.monthly_data['year'] = (
			pd.DatetimeIndex(self.monthly_data['date'])
			.year
		)
		self.monthly_data = self.monthly_data.drop(['date'], axis=1)

		# Take the mean of monthly data and merge with annual data
		mean_from_monthly = (
			self.monthly_data
			.groupby(['area', 'year'])
			.mean()
			.reset_index()
			.rename(columns={'houses_sold': 'average_houses_sold'})
		)
		self.yearly_data = (
			pd.merge(self.yearly_data, mean_from_monthly,
					 on=['area', 'year'],
					 how='inner')
		)
		self.yearly_data = self.yearly_data.drop(['date'], axis=1)

		# Encode and scale features
		self.yearly_data['area'] = (
			encoder.fit_transform(self.yearly_data['area'])
		)

	def split_train_and_test(self, scale=False, scaler=StandardScaler()):
		y = self.yearly_data['average_price']
		X = self.yearly_data.drop(['average_price'], axis=1)

		if scale:
			X = scaler.fit_transform(X)

		return train_test_split(X, y, train_size=0.7)


class HousingPricesPredictor:
	model = None

	def __init__(self):
		self.model = KNeighborsRegressor(n_neighbors=3)

	def train(self, X_train, y_train):
		self.model.fit(X_train, y_train)
		return self.model.score(X_train, y_train)

	def test(self, X_test, y_test):
		predictions = self.model.predict(X_test)
		return sqrt(mean_squared_error(y_train, train_predictions))

	def export(self, file_name):
		with open(file_name, 'wb') as output_file:
			pickle.dump(self.model, output_file)


def main():
	yearly_data_path = 'data/london_yearly_housing.csv'
	monthly_data_path = 'data/london_monthly_housing.csv'

	preprocessor = HousingPricesDataPreprocessor(yearly_data_path,
											     monthly_data_path)
	preprocessor.preprocess()
	X_train, X_test, y_train, y_test = preprocessor.split_train_and_test()

	model = HousingPricesPredictor()
	model.train(X_train, y_train)
	model.export('model.pkl')

if __name__ == '__main__':
	main()
