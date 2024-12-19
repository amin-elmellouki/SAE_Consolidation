var table;
window.addEventListener('load', () => {
    table = document.querySelector("table");
})

function sendToConso() {
    let headers = table.querySelectorAll("th")
    let lines = table.querySelectorAll("tbody tr");
    
    let consos = new Map();

    for (let i = 0; i < lines.length; i++) {
        let columns = lines[i].querySelectorAll("td")
        
        for (let j = 0; j < columns.length; j++) {
            let checkbox = columns[j].querySelector("input[type=checkbox]");

            if (checkbox && checkbox.checked) {
                if (consos.has(headers[j].innerText)) {
                    consos.get(headers[j].innerText).push(columns[0].innerText);
                } else {
                    consos.set(headers[j].innerText, [columns[0].innerText]);
                }
            }
        }
    }  

    let consosObject = Object.fromEntries(consos);
    fetch('/compte_rendu/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(consosObject),
    })
    .then(response => {
        if (response.redirected) {
            // Si le serveur a renvoyé une redirection
            window.location.href = response.url;
        } else {
            return response.text(); // Récupérer le contenu HTML
        }
    })
    .then(html => {
        document.body.innerHTML = html; // Remplacer le contenu de la page
    })
    .catch(error => console.error('Erreur lors de la requête POST :', error));
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
