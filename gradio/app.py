import gradio as gr
import numpy as np
import pickle
from collections import OrderedDict


TICKET_CLASSES = {
    'Upper': 1,
    'Middle': 2,
    'Lower': 3,
}
SEXES = {
    'Female': 0,
    'Male': 1,
}
TITLES = {
    'Master': 0,
    'Miss': 1,
    'Mr': 2,
    'Mrs': 3,
}
EMBARKED = {
    'Cherbourg': 0,
    'Queenstown': 1,
    'Southampton': 2,
}
AGE_BUCKETS = OrderedDict({
    5: 0,
    10: 1,
    20: 2,
    30: 3,
    40: 4,
    100: 5,
})


class TitanicApp(object):

    def __init__(self, model_dir):
        self.form_pclass = None
        self.form_sex = None
        self.form_title = None
        self.form_embarked = None
        self.form_age = None
        self.form_sibsp = None
        self.form_parch = None
        self.model = TitanicApp.load_model(model_dir)
        self.output = None

    def render_page(self):
        self.form_pclass = gr.Radio(
            label='Ticket Class',
            choices=list(TICKET_CLASSES.keys()),
            type='value',
            # value='Uppxer'
        )
        self.form_sex = gr.Radio(
            label='Sex',
            choices=list(SEXES.keys()),
            type='value',
            value='Female'
        )
        self.form_title = gr.Radio(
            label='Your Title',
            choices=list(TITLES.keys()),
            type='value',
            value='Miss',
        )
        self.form_embarked = gr.Radio(
            label='Port of Embarkation',
            choices=list(EMBARKED.keys()),
            type='value',
            value='Cherbourg',
        )
        self.form_age = gr.Slider(
            label='Age',
            minimum=0,
            maximum=100,
            step=1,
            value=0
        )
        self.form_sibsp = gr.Slider(
            label='Number of siblings or spouses aboard with you',
            minimum=0,
            maximum=10,
            step=1,
            value=0
        )
        self.form_parch = gr.Slider(
            label='Number of parents or children aboard with you',
            minimum=0,
            maximum=10,
            step=1,
            value=0
        )
        self.output = 'label'

        inputs = [
            self.form_pclass,
            self.form_sex,
            self.form_title,
            self.form_embarked,
            self.form_age,
            self.form_sibsp,
            self.form_parch
        ]
        front = gr.Interface(fn=self.get_prediction,
                           inputs=inputs,
                           outputs=self.output)
        front.launch()


    def get_prediction(self, *args):
        pclass = TICKET_CLASSES.get(args[0]) or 1
        sex = SEXES.get(args[1]) or 0
        title = TITLES.get(args[2])
        embarked = EMBARKED.get(args[3])
        age = int(args[4])
        sibsp = int(args[5])
        parch = int(args[6])

        # Age needs to be bucketed
        age_bucket = 0
        for k,v in AGE_BUCKETS.items():
            if age <= k:
                age_bucket = v
                break

        data = (
            np
            .array([pclass, sex, age_bucket, sibsp, parch, embarked, title])
            .reshape(1,-1)
        )
        res = self.model.predict(data)[0]

        if res == 1:
            output_text = 'Congrats! You survived!'
        else:
            output_text = 'Sorry, you died.'

        return output_text


    @staticmethod
    def load_model(model_dir):
        try:
            model = None
            with open(model_dir, 'rb') as file:
                model = pickle.load(file)
            return model
        except:
            print('Unable to load prediction model!')
            raise Exception


app = TitanicApp('../models/titanic_model.sav')
app.render_page()
