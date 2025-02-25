var loadedFiles;

function autoSetMat() {
    var comboBox = document.getElementById('matiere-select') 
    var options = comboBox.options;

    console.log(loadedFiles)
    for (file in loadedFiles) {
        for (option in options) {
            if (options[option].innerText == "") {
                continue;
            }

            if (loadedFiles[file].name.includes(options[option].innerText)) {
                console.log(options[option])
                comboBox.selectedIndex = option;
                return;
            }
        }
    }

    console.log("Pas trouvé")
}

function fileInputHandler(event, type) {
    const files = event.target.files;
    
    if (type === 'bilan') {
        uploadFiles(files, loadBilanUrl);
    } else {
        loadedFiles = files;
        autoSetMat();
    }
}

function dropHandler(ev, type) {
    console.log("File(s) dropped");
    
    ev.preventDefault();

    let files;
    if (ev.dataTransfer.items) {
        files = [...ev.dataTransfer.items].map(item => item.getAsFile());
    } else {
        files = [...ev.dataTransfer.files];
    }
    
    console.log(type)
    if (type === 'bilan') {
        uploadFiles(files, loadBilanUrl);
    } else {
        loadedFiles = files;
        autoSetMat();
    }
}

function uploadFiles(files, url, mat=null) {
    let formData = new FormData();
    for (let file of files) {
        formData.append('files', file);
    }

    console.log(mat)
    if (mat) {
        console.log("Ajout de matiere dans le formulaire")
        formData.append('matiere', mat)
    }

    fetch(url, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
    }).then(response => {
        if (response.ok) {
            console.log("Files uploaded successfully.");
            showMessage((url == loadBilanUrl) ? ("bilan") : ("qcm"), false)
        } else {
            console.error("File upload failed.");
            showMessage((url == loadBilanUrl) ? ("bilan") : ("qcm"), true)
        }
    }).catch(error => {
        console.error("Error:", error);
        showMessage((url == loadBilanUrl) ? ("bilan") : ("qcm"), true)
    });
}

function showMessage(type, err) {
    document.getElementById(`${(err) ? ("err") : ("succ")}-${type}`).style.display = 'flex';
    setTimeout(() => {
        location.reload();
    }, 3000);
}

function sendQcm() {
    var e = document.getElementById('matiere-select')
    uploadFiles(loadedFiles, loadQcmUrl, e.options[e.selectedIndex].text);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', function() {
    const semaineButton = document.querySelector('.bilan-button');
    
    if (semaineButton) {
        // État initial
        let isAsc = false;
        
        semaineButton.addEventListener('click', function() {
            isAsc = !isAsc;
            this.setAttribute('data-sort', isAsc ? 'asc' : 'desc');
            
            const scrollable = document.querySelector('.bilan-scrollable');
            const anchors = Array.from(scrollable.querySelectorAll('a'));
            
            anchors.sort((a, b) => {
                // On extrait le texte de la date (avant la parenthèse s'il y en a une)
                const getDateText = (element) => {
                    return element.textContent.trim().split('(')[0].trim();
                };
                
                const aDateText = getDateText(a);
                const bDateText = getDateText(b);
                
                // Si vos dates sont au format YYYY-MM-DD ou similaire, cette comparaison simple fonctionnera
                return isAsc ? aDateText.localeCompare(bDateText) : bDateText.localeCompare(aDateText);
            });
            
            // Rafraîchir l'affichage
            scrollable.innerHTML = '';
            anchors.forEach(anchor => scrollable.appendChild(anchor));
        });
    }
});