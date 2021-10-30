from flask import Flask, render_template, request
import csv

app = Flask(__name__)

with open('database.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    allData = list(reader)
    headings = allData[0]
    del allData[0]
    data =  allData
    str_data = str(data)

@app.route('/')
def index():
    return render_template('index.html', data=data, headings=headings)

@app.route('/phoneApp', methods=['GET', 'POST'])
def parse_request():
    if request.method == 'POST':
        try:
            message = request.form['message']
            return save_msg(message)
        except:
            print("Error with message request")
    else:
        return str_data, 200, {'Content-Type': 'text/plain; charset=utf-8'}

def save_msg(message):
    with open('messages.log', 'w') as f:
        f.write(message + '\n')
    return 'message saved'

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
