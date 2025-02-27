document.addEventListener('DOMContentLoaded', function() {
    const absentButtons = document.querySelectorAll('.absence');

    absentButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();

            if (!this.classList.contains('marked-absent')) {
                this.classList.add('marked-absent');
                this.innerText = "Absent";
            } else {
                this.classList.remove('marked-absent');
                this.innerText = "Présent";
            }

            const etudiantId = button.getAttribute('data-etudiant');
            const consoId = button.getAttribute('data-conso');
            
            fetch('/set_absent/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    etudiant_id: etudiantId,
                    conso_id: consoId
                })
            })
            .then(response => {
                console.log('Response Status:', response.status); 
                return response.json();
            })
            .catch(error => console.error('Error:', error));
        }, 0);
    });
});

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
