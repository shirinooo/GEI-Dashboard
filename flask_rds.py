from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import psycopg
from OpenSSL import SSL
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

load_dotenv()

# Replace these with your AWS RDS database credentials
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# The function to get the submission count from the database
def get_submission_count():
    try:
        # Connect to the database
        connection = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        # Create a cursor
        cursor = connection.cursor()

        # Execute a query to get the count 
        cursor.execute("SELECT count FROM total_submissions")

        # Fetch the result
        count = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return count[0][0]

    except Exception as e:
        print(f"Error: {e}")
        return None

# Route for the total_submission chart in dashboard
@app.route('/submission', methods=['GET', 'POST'])
def total_submission_dashboard():
    count = get_submission_count()

    if count is not None:
        # Create the response in the specified format
        response_data = {
            "count": count
        }
        # Convert the response to JSON and return
        return jsonify(response_data)
    else:
        return jsonify({"error": "Failed to fetch data from the database"}), 500


# Function to get the average learning hours from database
def get_learning_hours():
    try:
        # Connect to the database
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as connection:

            # Create a cursor
            cursor = connection.cursor()

            # Execute a query to get the count 
            cursor.execute("SELECT country, hours FROM learning_hours")

            # Fetch the result
            data_set = cursor.fetchall()
            
            dict = [{"country": v[0], "hours": v[1]} for v in data_set]
            result_dict = {
                "datasets": dict
            }

        return result_dict

    except Exception as e:
        print(f"Error: {e}")
        return None

# Route for the learning_hours chart in dashboard
@app.route('/learning_hours', methods=['GET', 'POST'])
def learning_hours_dashboard():
    data_sets = get_learning_hours()

    if data_sets is not None:
        # Create the response in the specified format
        response_data = data_sets
        # Convert the response to JSON and return
        return jsonify(response_data)
    else:
        return jsonify({"error": "Failed to fetch data from the database"}), 500
    
# Function to get escs values from database
def get_escs_value():
    try:
        # Connect to the database
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as connection:

            # Create a cursor
            cursor = connection.cursor()

            # Execute a query to get the count 
            cursor.execute("SELECT id, value FROM escs")

            # Fetch the result
            data_set = cursor.fetchall()
            
            dict = [{"id": v[0], "value": v[1]} for v in data_set]
            result_dict = {
                "datasets": dict
            }

        return result_dict

    except Exception as e:
        print(f"Error: {e}")
        return None

# Route for the escs_value chart in dashboard
@app.route('/escs_value', methods=['GET', 'POST'])
def escs_value_dashboard():
    data_sets = get_escs_value()

    if data_sets is not None:
        # Create the response in the specified format
        response_data = data_sets
        # Convert the response to JSON and return
        return jsonify(response_data)
    else:
        return jsonify({"error": "Failed to fetch data from the database"}), 500

# Function to get EESB values from the database
def get_eesb():
    try:
        # Connect to the database
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as connection:

            # Create a cursor
            cursor = connection.cursor()

            # Execute a query to get the count 
            cursor.execute("SELECT id, x, y, submissions FROM eesb")

            # Fetch the result
            data_set = cursor.fetchall()
            
            data_set_dict = [{"id": v[0], "data": [{"x": v[1], "y": v[2], "submissions": v[3]}]} for v in data_set]
            result_dict = {
                "datasets": data_set_dict
            }

        return result_dict

    except Exception as e:
        print(f"Error: {e}")
        return None 

# Route for the eesb chart in dashboard
@app.route('/eesb', methods=['GET', 'POST'])
def eesb_dashboard():
    data_sets = get_eesb()

    if data_sets is not None:
        # Create the response in the specified format
        response_data = data_sets
        # Convert the response to JSON and return
        return jsonify(response_data)
    else:
        return jsonify({"error": "Failed to fetch data from the database"}), 500

# Function to get submissions over time from database
def get_submission_over_time():
    try:
        # Connect to the database
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as connection:

            # Create a cursor
            cursor = connection.cursor()

            # Execute a query to get the count 
            cursor.execute("""with sot_time as (
                                    select 
                                        x
                                        , y - lag(y) over (order by cast(x as time)) as submission_count
                                    from submissions_running_total
                                    where cast(x as time) between '11:07' and '11:30'
                                )
                                select *
                                from sot_time
                                where submission_count is not null""")

            # Fetch the result
            data_set = cursor.fetchall()
            
            data_hourly_counts = [{"x": f"{v[0]}", "y": v[1]} for v in data_set]
            
            data_set_dict = [{
                "id": "Submissions",
                "data": data_hourly_counts
            }]
            result_dict = {
                "datasets": data_set_dict
            }

        return result_dict

    except Exception as e:
        print(f"Error: {e}")
        return None
    
# Route for the submission_over_time chart in dashboard
@app.route('/submission_over_time', methods=['GET', 'POST'])
def submission_over_time_dashboard():
    data_sets = get_submission_over_time()

    if data_sets is not None:
        # Create the response in the specified format
        response_data = data_sets
        # Convert the response to JSON and return
        return jsonify(response_data)
    else:
        return jsonify({"error": "Failed to fetch data from the database"}), 500


if __name__ == '__main__':
    context=("cert.pem", "key.pem")
    app.run(debug=True, host="0.0.0.0", port=5000, ssl_context=context)