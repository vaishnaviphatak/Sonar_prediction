from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load the trained model
try:
    model = joblib.load('model.pkl')
except FileNotFoundError:
    model = None
    print("Warning: model.pkl not found. Please run train_model.py first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded on the server.'}), 500

    try:
        data = request.json
        input_string = data.get('features', '')

        # Process the comma-separated string into a list of floats
        input_list = [float(i.strip()) for i in input_string.split(',') if i.strip()]

        if len(input_list) != 60:
            return jsonify({'error': f'Expected 60 features, but got {len(input_list)}.'}), 400

        # Change the input data to a numpy array
        input_data_as_numpy_array = np.asarray(input_list)

        # Reshape the np array as we are predicting for one instance
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

        # Make prediction
        prediction = model.predict(input_data_reshaped)
        
        result = 'Rock' if prediction[0] == 'R' else 'Mine'
        
        return jsonify({
            'prediction': result,
            'message': f'The object is a {result.lower()}.'
        })
    except ValueError:
        return jsonify({'error': 'Invalid input format. Ensure all values are comma-separated numbers.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
