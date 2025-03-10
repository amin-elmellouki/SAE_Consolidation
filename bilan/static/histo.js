function createQCMHistory(data) {
    const table = document.createElement('table');
    table.className = 'info-table';
    table.style.display = 'none';
    
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headerCell = document.createElement('th');
    headerCell.textContent = 'Historique QCM ' + data.matiere;
    headerRow.appendChild(headerCell);
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    const tbody = document.createElement('tbody');
    tbody.className = 'matiere-info';
    
    data.notes.forEach(note => {
        const row = document.createElement('tr');
        row.className = 'skibidi';
        
        const cell = document.createElement('td');
        const span = document.createElement('span');
        span.setAttribute('data-note', note);
        span.classList.add('tag');
        span.textContent = note;
        
        const value = parseFloat(note);
        if (value >= 15) {
            span.classList.add('green');
        } else if (value >= 10) {
            span.classList.add('yellow');
        } else if (value >= 5) {
            span.classList.add('orange');
        } else {
            span.classList.add('red');
        }
        
        cell.appendChild(span);
        row.appendChild(cell);
        tbody.appendChild(row);
    });
    
    table.appendChild(tbody);
    return table;
}

function createConsoHistoryTable(historiqueData) {
    const table = document.createElement('table');
    table.className = 'info-table';
    
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headerCell = document.createElement('th');
    headerCell.colSpan = 500;
    headerCell.textContent = 'Historique des conso.';
    headerRow.appendChild(headerCell);
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    const tbody = document.createElement('tbody');
    
    Object.entries(historiqueData).forEach(([matiere, consos]) => {
        const row = document.createElement('tr');
        const matiereCell = document.createElement('td');
        matiereCell.textContent = matiere;
        row.appendChild(matiereCell);
        
        if (Array.isArray(consos)) {
            consos.forEach(conso => {
                const consoCell = document.createElement('td');
                consoCell.innerHTML = conso;
                row.appendChild(consoCell);
            });
        } else {
            const consoCell = document.createElement('td');
            consoCell.innerHTML = consos; 
            row.appendChild(consoCell);
        }
        
        tbody.appendChild(row);
    });
    
    table.appendChild(tbody);
    return table;
}

function attachHoverEventListeners() {
    let infoTableContainer = document.getElementById('info-table-container');
    if (!infoTableContainer) {
        infoTableContainer = document.createElement('div');
        infoTableContainer.id = 'info-table-container';
        infoTableContainer.style.position = 'fixed';
        infoTableContainer.style.zIndex = '1000';
        document.body.appendChild(infoTableContainer);
    }

    document.querySelectorAll('.student-info').forEach(cell => {
        const newCell = cell.cloneNode(true);
        cell.parentNode.replaceChild(newCell, cell);
    });
    
    document.querySelectorAll('tr').forEach(row => {
        if (row.style.display !== 'none') {
            const cells = row.querySelectorAll('.student-info');
            cells.forEach(cell => {
                cell.addEventListener('mouseenter', function() {
                    const jsonData = this.dataset.history;
                    const historiqueData = this.dataset.historique; 
                    const matiereName = this.dataset.matiere || '';
                    const currentNote = this.dataset.currentNote || this.textContent.trim();
                    
                    let infoTable;

                    if (jsonData) {
                        try {
                            const notes = JSON.parse(jsonData);
                            if (notes.length > 0) {
                                infoTable = createQCMHistory({
                                    matiere: matiereName,
                                    notes: notes,
                                    currentNote: currentNote
                                });
                            }
                        } catch (error) {
                            console.error("Error parsing QCM JSON data:", error);
                        }
                    }

                    if (historiqueData) {
                        try {
                            const historique = JSON.parse(historiqueData);
                            if (Object.keys(historique).length > 0) {
                                infoTable = createConsoHistoryTable(historique); 
                            }
                        } catch (error) {
                            console.error("Error parsing historique JSON data:", error);
                        }
                    }
                    
                    if (infoTable) {
                        infoTable.style.position = 'fixed';
                        infoTable.style.display = 'table';
                        infoTable.style.boxShadow = '0px 4px 8px rgba(0, 0, 0, 0.2)';

                        const rect = this.getBoundingClientRect();
                        infoTable.style.left = rect.left + 'px';
                        infoTable.style.top = rect.bottom + 5 + 'px';

                        infoTableContainer.appendChild(infoTable);
                    }
                });
            
                cell.addEventListener('mouseleave', function() {
                    const infoTables = infoTableContainer.querySelectorAll('.info-table');
                    infoTables.forEach(table => {
                        table.style.display = 'none';
                    });
                });
            });
        }
    });
}
