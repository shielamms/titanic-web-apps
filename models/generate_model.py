from .preprocessor import HousingPricesDataPreprocessor
from .predictor import HousingPricesPredictor


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
