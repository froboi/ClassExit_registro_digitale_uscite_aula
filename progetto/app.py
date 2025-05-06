from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/class_students', methods=['POST'])
def add_class():
    class_name = request.form['class_name']
    # Salva la classe nel database
    db.insert({'class_name': class_name, 'students': []})
    # Reindirizza alla pagina de5ll'elenco studenti
    return redirect(url_for('class_students', class_name=class_name))

@app.route('/class/<class_name>')
def class_students(class_name):
    # Recupera la classe dal database
    Class = Query()
    class_data = db.search(Class.class_name == class_name)
    if class_data:
        students = class_data[0].get('students', [])
    else:
        students = []
    return render_template('class_students.html', class_name=class_name, students=students)

if __name__ == '__main__':
    app.run(debug=True)