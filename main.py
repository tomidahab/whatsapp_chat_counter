from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaaaaaadaksmqoe'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


def leer_info_ios(ejs):
        
    linea = ejs.readline()        
    linea = str(linea)
    linea = linea.replace("]",":")
    if linea and linea.count(":") >= 4:
        lista = linea.split(":")
    elif linea:
        lista = ["","","NADA","NADA",""]
    else:
        lista = ["","","","",""]
    return lista

def leer_info(ejs):
        
    linea = ejs.readline()        
    linea = str(linea)
    linea = linea.replace(":","-")
    if linea and linea.count("-") >= 3:
        lista = linea.split("-")
    elif linea:
        lista = ["","","NADA","",""]
    else:
        lista = ["","","","",""]
    return lista
    

def chats_wpp(archivo):
    res = ""
    datos = leer_info(archivo)
    apellido = datos[2]
    diccionario = {}
    while apellido != "":
        if apellido in diccionario:
            diccionario[apellido] += 1
        else:
            diccionario[apellido] = 1
        datos = leer_info(archivo)
        apellido = datos[2]
    lista = sorted(diccionario.items(), key=lambda kv: kv[1], reverse = True)
    for i in lista:
        res += "{}: {} mensajes\n".format(i[0],i[1])
    return res

def chats_wpp_ios(archivo):
    res = ""
    datos = leer_info_ios(archivo)
    apellido = datos[3]
    diccionario = {}
    while apellido != "":
        if apellido in diccionario:
            diccionario[apellido] += 1
        else:
            diccionario[apellido] = 1
        datos = leer_info_ios(archivo)
        apellido = datos[3]
    lista = sorted(diccionario.items(), key=lambda kv: kv[1], reverse = True)
    for i in lista:
        res += "{}: {} mensajes\n".format(i[0],i[1])
    return res





#@app.route('/home', methods=['GET',"POST"])
@app.route('/', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.seek(0)
        return render_template('result.html',res=chats_wpp_ios(file))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)