import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
from baseDatos import pruebaHuellaDf, credenciales, datosConsolidados
import openpyxl
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

        return 'Los datos se han cargado correctamente'
    else:
        return 'No file uploaded'

@app.route('/datoshuella', methods=['GET'])
def datosinstitucion():
    cred = credenciales('admin')
    paciente_data = datosConsolidados(cred)
    return jsonify(paciente_data)

if __name__ == '__main__':
    # app.run()
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))
