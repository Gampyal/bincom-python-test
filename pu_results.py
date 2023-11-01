from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Establish a connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234567890",
    database="election"
)
myCursor = db.cursor()

# Move your database queries into separate functions
def get_polling_units():
    myCursor.execute("SELECT uniqueid, polling_unit_name FROM polling_unit")
    return myCursor.fetchall()

def find_scores(polling_uuid):
    announced_pu_results_query = "SELECT party_abbreviation, party_score FROM announced_pu_results WHERE polling_unit_uniqueid = %s"
    try:
        myCursor.execute(announced_pu_results_query, (polling_uuid,))
        announced_pu_data = myCursor.fetchall()
        announced_pu_scores = {abbreviation: score for abbreviation, score in announced_pu_data}
        return announced_pu_scores
    except mysql.connector.Error as e:
        print("Error executing query: ", e)
        return None

def get_polling_unit_name_by_id(polling_uuid):
    polling_units = get_polling_units()
    for id, name in polling_units:
        if id == polling_uuid:
            return name
    return None



@app.route('/')
def index():
    polling_units = get_polling_units()
    return render_template('pu_listing.html', polling_units=polling_units)

@app.route('/display_results', methods=['POST'])
def display_results():
    polling_uuid = int(request.form['polling_unit'])
    polling_unit_name = get_polling_unit_name_by_id(polling_uuid)
    announced_pu_results_data = find_scores(polling_uuid)
    return render_template('pu_results.html', polling_unit_name=polling_unit_name, results=announced_pu_results_data)









if __name__ == '__main__':
    app.run(debug=True)
