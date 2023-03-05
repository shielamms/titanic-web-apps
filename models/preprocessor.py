import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


class Preprocessor(object):
	_data = None

	def preprocess(self):
		return NotImplemented


class HousingPricesDataPreprocessor(Preprocessor):
	_monthly_data = None

	def __init__(self, yearly_data_path, monthly_data_path):
		self._data = pd.read_csv(yearly_data_path)
		self._monthly_data = pd.read_csv(monthly_data_path)		

	def preprocess(self, encoder=LabelEncoder()):
		# Convert date column type to datetime
		self._data['date'] = pd.to_datetime(self._data['date'])
		self._monthly_data['date'] = pd.to_datetime(self._monthly_data['date'])

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
		]
		self._data = self._data[relevant_yearly_features]
		self._monthly_data = self._monthly_data[relevant_monthly_features]

		# Get the year from the date
		self._data = (
			self._data.dropna(
				subset=['median_salary', 'population_size'])
		)
		self.yearly_data['year'] = (
			pd.DatetimeIndex(self.yearly_data['date'])
			.year
		)
		self._monthly_data['year'] = (
			pd.DatetimeIndex(self._monthly_data['date'])
			.year
		)
		self._monthly_data = self._monthly_data.drop(['date'], axis=1)

		# Take the mean of monthly data and merge with annual data
		mean_from_monthly = (
			self._monthly_data
			.groupby(['area', 'year'])
			.mean()
			.reset_index()
		)
		self._data = (
			pd.merge(self._data, mean_from_monthly,
					 on=['area', 'year'],
					 how='inner')
		)
		self._data = self._data.drop(['date'], axis=1)

		# Encode and scale features
		self._data['area'] = (
			encoder.fit_transform(self._data['area'])
		)

	def split_train_and_test(self, scale=False, scaler=StandardScaler()):
		y = self._data['average_price']
		X = self._data.drop(['average_price'], axis=1)

		if scale:
			X = scaler.fit_transform(X)

		return train_test_split(X, y, train_size=0.7)
