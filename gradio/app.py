import gradio as gr
import pickle


def predict(median_salary, population_size, houses_sold, year):
	with open('../models/titanic_model.sav', 'rb') as file:
		model = pickle.load(file)
		return (
			model.predict(
				[[median_salary, population_size, houses_sold, year]])
		)


median_salary = gr.Slider(0, 50000)
population_size = gr.Slider(0, 100000)
houses_sold = gr.Slider(0, 100)
year = gr.Slider(1990, 2020)
output = gr.Textbox()

app = gr.Interface(fn=predict,
				   inputs=[median_salary, population_size, houses_sold, year],
				   outputs=output)

app.launch()