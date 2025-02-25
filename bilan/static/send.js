var table;
window.addEventListener('load', () => {
    table = document.querySelector("table");
})

function sendToConso() {
    let body = new Map();
    body.set("date", table.dataset.date)
    
    let conso = new Map();

    let checkboxColumns = table.querySelectorAll(".checkbox-column")

    for (let i = 0; i < checkboxColumns.length; i++) {
        let checkboxColumn = checkboxColumns[i]  
        let checkbox = checkboxColumn.querySelector("input[type=checkbox]");
    
        if (checkbox.checked) {
            let matiere = checkboxColumn.dataset.matiere
            let numE = checkboxColumn.dataset.nume

            if (conso.has(matiere)) {
                conso.get(matiere).push(numE)
            } else {
                conso.set(matiere, new Array(numE))
            }
        }
    } 
    
    body.set("conso", Object.fromEntries(conso));
    let bodyObject = Object.fromEntries(body);

    console.log(JSON.stringify(bodyObject))

    fetch('/compte_rendu/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(bodyObject),
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.text();
        }
    })
    .then(html => {
        document.body.innerHTML = html;
        setUpTables();
    })
    .catch(error => console.error('Erreur lors de la requête POST :', error));
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
