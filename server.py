from flask import Flask, render_template
import csv
app = Flask(__name__)

with open('database.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    allData = list(reader)
    headings = allData[0]
    del allData[0]
    data =  allData

@app.route('/')
def index():
    return render_template('index.html', data=data, headings=headings)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
