from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define your database connection parameters
db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "vizvacons123",
    # Change this if your database is hosted elsewhere
    "host": "tmsdb.cnqltqgk9yzu.us-east-1.rds.amazonaws.com",
    "port": "5432"
}


@app.route('/', methods=['GET'])
def get_data():
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Execute a query to retrieve data (modify the query as needed)
        query = "SELECT * FROM email_table"
        cursor.execute(query)
        data = cursor.fetchall()

        # Convert the data to a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/assign', methods=['POST'])
def assign_task():
    try:
        data = request.json
        task_id = data.get("task_id")
        assignee = data.get("assignee")

        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Update the database with the assigned assignee for the specified task_id
        query = "UPDATE email_table SET assignee = %s WHERE task_id = %s"
        cursor.execute(query, (assignee, task_id))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return jsonify({"message": "Task assigned successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)