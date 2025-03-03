document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('button.delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            deleteStudent(this);
        });
    });
});
  
function deleteStudent(buttonElement) {
    const etudiantId = buttonElement.dataset.etudiant;
    const consoId = buttonElement.dataset.conso;
    
    fetch(`/delete_stu/${etudiantId}/${consoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie("csrftoken"),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            const table = document.querySelector('table');
            const date = table.dataset.date;
            window.location.href = '/conso/' + date + '/';
        } else {
            return response.text();
        }
    })
    .then(html => {
        if (html) {
            document.body.innerHTML = html;
            setUpTables();
        }
    })
    .catch(error => console.error('Erreur lors de la requête POST :', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
            }
        }
    }
    return cookieValue;
}