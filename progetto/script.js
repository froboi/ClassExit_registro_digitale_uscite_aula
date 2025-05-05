document.addEventListener('DOMContentLoaded', () => {
    const exitForm = document.getElementById('exitForm');
    const entryForm = document.getElementById('entryForm');
    const exitLog = document.getElementById('exitTable').getElementsByTagName('tbody')[0];

    let exitRecords = [];

    exitForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const studentName = document.getElementById('studentName').value.trim();
        const exitTime = document.getElementById('exitTime').value;

        // Controlla se il nome dello studente è vuoto
        if (!studentName) {
            alert("Questa casella non può rimanere incompilata.");
            return;
        }

        // Aggiungi l'uscita al registro
        const record = {
            name: studentName,
            exit: exitTime,
            entry: null
        };
        exitRecords.push(record);
        updateLog();
        
        // Resetta il modulo
        exitForm.reset();
    });

    entryForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const entryStudentName = document.getElementById('entryName').value.trim();
        const entryTime = document.getElementById('entryTime').value;

        // Controlla se il nome dello studente è vuoto
        if (!entryStudentName) {
            alert("Questa casella non può rimanere incompilata.");
            return;
        }

        // Trova il record corrispondente e aggiorna l'ora di rientro
        const record = exitRecords.find(r => r.name === entryStudentName && r.entry === null);
        if (record) {
            record.entry = entryTime;
            updateLog();
        } else {
            alert("Nessun record trovato per questo studente.");
        }

        // Resetta il modulo
        entryForm.reset();
    });

    function updateLog() {
        // Pulisci il registro esistente
        exitLog.innerHTML = '';
        // Aggiungi i record al registro
        exitRecords.forEach(record => {
            const row = exitLog.insertRow();
            row.insertCell(0).textContent = record.name;
            row.insertCell(1).textContent = record.exit;
            row.insertCell(2).textContent = record.entry ? record.entry : 'Non rientrato';
        });
    }
});