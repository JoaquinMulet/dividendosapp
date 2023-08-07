# app.py
from flask import Flask, request, send_file
import csv
import io
import json

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json['data']
    
    # Aquí ajustamos para manejar el texto directamente
    formatted_data = "{" + data.split("{", 1)[1]  # Añadir "{" al inicio
    if not formatted_data.endswith("},"):
        formatted_data += "}"  # Añadir "}" al final si es necesario
    
    try:
        json_data = json.loads(formatted_data)['listaResult']
    except json.JSONDecodeError:
        return "Error en el formato del texto ingresado", 400

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=json_data[0].keys())
    writer.writeheader()
    for row in json_data:
        writer.writerow(row)

    output.seek(0)
    return send_file(output, as_attachment=True, download_name="data.csv", mimetype="text/csv")

if __name__ == '__main__':
    app.run(debug=True)
