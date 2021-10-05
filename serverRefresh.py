
def refresh():

    with open("server.py", 'w', newline='') as f:
        f.write("from flask import Flask, render_template\n")
        f.write("import csv\n")
        f.write("app = Flask(__name__)\n")
        f.write("\n")
        f.write("with open('database.csv', 'r', newline='') as f:\n")
        f.write("    reader = csv.reader(f)\n")
        f.write("    allData = list(reader)\n")
        f.write("    headings = allData[0]\n")
        f.write("    del allData[0]\n")
        f.write("    data =  allData\n")
        f.write("\n")
        f.write("@app.route('/')\n")
        f.write("def index():\n")
        f.write("    return render_template('index.html', data=data, headings=headings)\n")
        f.write("\n")
        f.write("if __name__ == '__main__':\n")
        f.write("    app.run(debug=True, port=80, host='0.0.0.0')\n")


