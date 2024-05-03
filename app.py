from flask import Flask, render_template, request
import psycopg2
import pandas as pd

from baseDatos import pruebaHuellaDf, credenciales

app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file.filename != '':
        # Save the uploaded file temporarily
        file.save(file.filename)

        # Read data from the Excel file
        df = pd.read_excel(file.filename)

        cred = credenciales("admin")
        pruebaHuellaDf(cred,df)

        return 'File uploaded and data inserted successfully!'
    else:
        return 'No file uploaded'


if __name__ == '__main__':
    app.run(debug=True)
