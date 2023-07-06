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


def leer_info(ejs):
        
    linea = ejs.readline()
    linea = linea.replace(":","-")
    if linea and linea.count("-") >= 3:
        lista = linea.split("-")
    elif linea:
        lista = ["","","NADA","",""]
    else:
        lista = ["","","","",""]
    return lista
    

def chats():
    res = ""
    path = os.getcwd()
    path += "/static/files/out.txt"
    with open(path, 'rt') as archivo:

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
        print(diccionario)
        lista = sorted(diccionario.items(), key=lambda kv: kv[1], reverse = True)
        for i in lista:
            #print("{}: {} mensajes".format(i[0],i[1]))
            res += "{}: {} mensajes\n".format(i[0],i[1])
    return res





#@app.route('/home', methods=['GET',"POST"])
@app.route('/', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename("out.txt"))) # Then save the file
        #return "File has been uploaded."
        print()
        return render_template('result.html',res=chats())
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)