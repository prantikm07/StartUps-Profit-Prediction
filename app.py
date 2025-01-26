from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)

# Initialize LabelEncoder and encode state values
state_encoder = LabelEncoder()
state_encoder.fit(['California', 'Florida', 'New York'])

@app.route('/', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        # Get the form inputs
        rd_spend = float(request.form['rd_spend'])
        admin = float(request.form['admin'])
        marketing_spend = float(request.form['marketing_spend'])
        state = request.form['state']

        # Encode the state
        encoded_state = state_encoder.transform([state])[0]

        # Prepare the inputs
        inputs = pd.DataFrame([[rd_spend, admin, marketing_spend, encoded_state]],
                              columns=['R&D Spend', 'Administration', 'Marketing Spend', 'State'])

        # Load the model
        model = pickle.load(open('model.pkl', 'rb'))

        # Predict
        prediction = model.predict(inputs)
        formatted_prediction = f"{prediction[0]:.2f}"

        return render_template('home.html', prediction=formatted_prediction)

    else:
        return render_template('home.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)
