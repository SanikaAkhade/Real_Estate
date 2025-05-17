import util
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all origins to access your API


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        if request.method == 'POST':
            # Ensure the request content type is application/json
            if request.content_type != 'application/json':
                return jsonify({'error': 'Content-Type must be application/json'}), 400

            # Extract JSON data from the request
            data = request.get_json()

            # Check if all required data is provided
            if not all(key in data for key in ['total_sqft', 'location', 'bhk', 'bath']):
                return jsonify({'error': 'Missing required data'}), 400

            # Extract input data from the JSON
            total_sqft = float(data['total_sqft'])
            location = data['location']
            bhk = int(data['bhk'])
            bath = int(data['bath'])

            # Get the estimated price using your model (ensure util.py is set up correctly)
            estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

            # Return the estimated price as a JSON response
            response = jsonify({'estimated_price': estimated_price})
            response.headers.add('Access-Control-Allow-Origin', '*')  # Add CORS headers
            return response

        elif request.method == 'GET':
            # You can return a simple message for GET requests
            return jsonify({'message': 'Please send a POST request with data to predict home price.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    print("Starting Python Flask For Home Price Prediction...")
    util.load_saved_artifacts()  # Ensure that your model and artifacts are loaded
    app.run(debug=True)

