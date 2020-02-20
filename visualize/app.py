import ast
from flask import Flask,jsonify,request
from flask import render_template

#Create Flask app and define global variables to store labels and values for visualization.
app = Flask(__name__)
words = []
counts = []

#implement updateData to parse data sent from spark and return correct status codes according to request form
@app.route('/updateData', methods=['POST'])
def update_data_from_spark():
    global words, counts
    if not request.form or 'words' not in request.form:
        return "error",400
    words = ast.literal_eval(request.form['words'])
    counts = ast.literal_eval(request.form['counts'])
    print("current words: " + str(words))
    print("current counts: " + str(counts))
    return "success",201

#Implement refresh function to update hashtag labels and counts
@app.route('/updateChart')
def refresh_hashtag_data():
    global words, counts
    print("current words: " + str(words))
    print("current data: " + str(counts))
    return jsonify(sWords=words, sCounts=counts)
@app.route("/")

#create functions to initialize hashtag page, render_chart function binds to homepage, and it uses global labels and values to show the chart.
def showChart():
    global words,counts
    counts = []
    words = []
    return render_template('chart.html', counts=counts, words=words)

#Implement main function to run flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
