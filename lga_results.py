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

def get_lga_list():
    myCursor.execute("SELECT lga_id, lga_name FROM lga")
    return myCursor.fetchall()

def get_lga_name_by_id(lga_id):
    query = "SELECT lga_name FROM lga WHERE lga_id = %s;"
    myCursor.execute(query, (lga_id,))
    lga_name = myCursor.fetchone()
    return lga_name[0] if lga_name else None

def get_polling_unit_unique_ids(lga_id):
    query = "SELECT uniqueid FROM polling_unit WHERE lga_id = %s;"
    myCursor.execute(query, (lga_id,))
    return [row[0] for row in myCursor.fetchall()]

def get_party_scores(polling_unit_unique_ids):
    party_scores = {}

    for id in polling_unit_unique_ids:
        query = "SELECT party_abbreviation, party_score FROM announced_pu_results WHERE polling_unit_uniqueid = %s"
        myCursor.execute(query, (id,))
        lga_result = myCursor.fetchall()

        for abbreviation, score in lga_result:
            if abbreviation in party_scores:
                party_scores[abbreviation] += score
            else:
                party_scores[abbreviation] = score

    return party_scores


@app.route('/')
def index():
    lga_list = get_lga_list()
    return render_template('lga_listing.html', lga_list=lga_list)

@app.route('/results', methods=['POST'])
def display_results():
    lga_id = int(request.form['lga_id'])
    lga_name = get_lga_name_by_id(lga_id)
    polling_unit_unique_ids = get_polling_unit_unique_ids(lga_id)
    party_scores = get_party_scores(polling_unit_unique_ids)
    return render_template('lga_results.html', lga_name=lga_name, party_scores=party_scores)




if __name__ == '__main__':
    app.run(debug=True)
