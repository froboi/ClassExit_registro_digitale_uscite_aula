from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessario per i messaggi flash

# Inizializzazione del database
db = TinyDB('database.json')
classes_table = db.table('classes')

@app.route('/')
def index():
    # Renderizza la pagina principale
    return render_template('index.html')

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

    Class = Query()
    existing_class = classes_table.get(Class.name == class_name)

    if not existing_class:
        flash(f'La classe "{class_name}" non esiste.', 'error')
        return redirect(url_for('index'))

    students_list = existing_class.get('students', [])
    
    # Controlla se lo studente esiste già per nome
    if any(s['name'] == student_name for s in students_list):
        flash(f'Lo studente "{student_name}" esiste già nella classe "{class_name}".', 'warning')
    else:
        # Aggiungi lo studente come oggetto con una lista vuota per i record
        new_student = {'name': student_name, 'records': []}
        students_list.append(new_student)
        classes_table.update({'students': students_list}, Class.name == class_name)
        flash(f'Studente "{student_name}" aggiunto con successo alla classe "{class_name}".', 'success')
    
    return redirect(url_for('class_students', class_name=class_name))

@app.route('/class/<class_name>/student/<student_name_url>/record_time', methods=['POST'])
def record_time(class_name, student_name_url):
    data = request.get_json()
    entry_time = data.get('entry_time')
    exit_time = data.get('exit_time')

    student_name = student_name_url 

    if not entry_time and not exit_time:
        return jsonify({'status': 'error', 'message': 'Devi fornire almeno un orario di entrata o di uscita.'}), 400

    Class = Query()
    target_class = classes_table.get(Class.name == class_name)

    if not target_class:
        return jsonify({'status': 'error', 'message': f'Classe "{class_name}" non trovata.'}), 404

    students_list = target_class.get('students', [])
    student_found = False
    for student_obj in students_list:
        if student_obj['name'] == student_name:
            new_record = {}
            if entry_time:
                new_record['entry_time'] = entry_time
            if exit_time:
                new_record['exit_time'] = exit_time
            
            if new_record:
                student_obj.setdefault('records', []).append(new_record)
            
            student_found = True
            break
    
    if not student_found:
        return jsonify({'status': 'error', 'message': f'Studente "{student_name}" non trovato nella classe "{class_name}".'}), 404

    classes_table.update({'students': students_list}, Class.name == class_name)
    return jsonify({'status': 'success', 'message': f'Orari per {student_name} salvati con successo.'})

if __name__ == '__main__':
    app.run(debug=True)