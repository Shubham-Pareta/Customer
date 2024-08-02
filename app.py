from flask import Flask, render_template, request, url_for
import joblib
import sqlite3

# Load the trained model
model = joblib.load('models/logisticregression.lb')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/project")
def project():
    return render_template('project.html')

@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        try:
            # Extract data from form submission
            age = int(request.form.get("age", 0))
            flight_distance = int(request.form.get("flight_distance", 0))
            inflight_entertainment = int(request.form.get("inflight-entertainment", 0))
            baggage_handling = int(request.form.get("baggage-handling", 0))
            cleanliness = int(request.form.get("cleanliness", 0))
            departure_delay = int(request.form.get("departure_delay", 0))
            arrival_delay = int(request.form.get("arrival_delay", 0))
            
            gender = 1 if request.form.get("gender") == "Male" else 0
            customer_type = 1 if request.form.get("customer-type") == "Loyal Customer" else 0
            travel_type = 1 if request.form.get("travel-type") == "Business Travel" else 0
            
            class_type_str = request.form.get("class-type")
            if class_type_str == "Economy":
                class_type = 0
            elif class_type_str == "Economy Plus":
                class_type = 1
            else:
                class_type = 2

            # Add placeholder for the extra feature
            extra_feature = 0  # Placeholder value for the additional feature

            # Process the data to match the model's expected feature count
            unseen_data = [[age, flight_distance, inflight_entertainment, baggage_handling, cleanliness,
                            departure_delay, arrival_delay, gender, customer_type, travel_type, class_type, extra_feature]]

            # Make prediction
            prediction = model.predict(unseen_data)[0]                   

            labels = {1: "SATISFIED", 0: "NOT-SATISFIED"}

            # Save the prediction and input data to the SQLite database
            conn = sqlite3.connect('predictions.db')
            cursor = conn.cursor()

            # Create table if not exists
            cursor.execute('''CREATE TABLE IF NOT EXISTS predictions
                              (age INTEGER, flight_distance INTEGER, inflight_entertainment INTEGER, 
                              baggage_handling INTEGER, cleanliness INTEGER, departure_delay INTEGER, 
                              arrival_delay INTEGER, gender INTEGER, customer_type INTEGER, 
                              travel_type INTEGER, class_type INTEGER, extra_feature INTEGER, prediction TEXT)''')
            
            # Insert data into the database
            cursor.execute('''INSERT INTO predictions (age, flight_distance, inflight_entertainment, 
                              baggage_handling, cleanliness, departure_delay, arrival_delay, gender, 
                              customer_type, travel_type, class_type, extra_feature, prediction) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (age, flight_distance, inflight_entertainment, baggage_handling, cleanliness, 
                          departure_delay, arrival_delay, gender, customer_type, travel_type, class_type, 
                          extra_feature, labels[prediction]))
            conn.commit()
            conn.close()

            return render_template('output.html', output=labels[prediction])
        except Exception as e:
            return f"An error occurred: {e}"

    return "Invalid request method."

if __name__ == "__main__":
    app.run(debug=True)
