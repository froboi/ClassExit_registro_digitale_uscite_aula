from flask import Flask, render_template, request, redirect, url_for, flash
from tinydb import TinyDB, Query

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessario per i messaggi flash

# Inizializzazione del database
db = TinyDB('database.json')
classes_table = db.table('classes')

@app.route('/')
def index():
    # Renderizza la pagina principale
    return redirect(url_for('index'))

@app.route('/add_or_access_class', methods=['POST'])
def add_or_access_class():
    class_name = request.form['class_name'].strip()
    if not class_name:
        flash('Il nome della classe non può essere vuoto.', 'error')
        return redirect(url_for('index'))

    # Controlla se la classe esiste già
    Class = Query()
    existing_class = classes_table.get(Class.name == class_name)

    if existing_class:
        # Se la classe esiste, reindirizza alla pagina degli studenti
        flash(f'Sei stato reindirizzato alla classe "{class_name}".', 'success')
        return redirect(url_for('class_students', class_name=class_name))
    else:
        # Se la classe non esiste, creala
        classes_table.insert({'name': class_name, 'students': []})
        flash(f'Classe "{class_name}" creata con successo.', 'success')
        return redirect(url_for('class_students', class_name=class_name))

@app.route('/class/<class_name>')
def class_students(class_name):
    # Recupera la classe dal database
    Class = Query()
    existing_class = classes_table.get(Class.name == class_name)

    if not existing_class:
        flash(f'La classe "{class_name}" non esiste.', 'error')
        return redirect(url_for('index'))

    # Mostra la lista degli studenti della classe
    students = existing_class.get('students', [])
    return render_template('class_students.html', class_name=class_name, students=students)

@app.route('/class/<class_name>/add_student', methods=['POST'])
def add_student(class_name):
    student_name = request.form['student_name'].strip()
    if not student_name:
        flash('Il nome dello studente non può essere vuoto.', 'error')
        return redirect(url_for('class_students', class_name=class_name))

    # Recupera la classe dal database
    Class = Query()
    existing_class = classes_table.get(Class.name == class_name)

    if not existing_class:
        flash(f'La classe "{class_name}" non esiste.', 'error')
        return redirect(url_for('index'))

    # Aggiungi lo studente alla classe
    students = existing_class.get('students', [])
    students.append(student_name)
    classes_table.update({'students': students}, Class.name == class_name)

    flash(f'Studente "{student_name}" aggiunto con successo alla classe "{class_name}".', 'success')
    return redirect(url_for('class_students', class_name=class_name))

if __name__ == '__main__':
    app.run(debug=True)