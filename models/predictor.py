import pickle
from math import sqrt

from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor


class Predictor(object):
	model = None

	def train(self):
		return NotImplemented

	def test(self):
		return NotImplemented

	def export(self):
		return NotImplemented


class HousingPricesPredictor(Predictor):

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
