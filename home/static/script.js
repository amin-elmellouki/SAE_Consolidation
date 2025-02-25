var loadedFiles = new Array();

function detectFileType(file) {
    return new Promise((resolve) => {
        let reader = new FileReader();
        reader.readAsText(file);

        reader.onload = () => {
            if (reader.result.startsWith("Nom complet de l’utilisateur")) {
                resolve("bilan");
            } else {
                resolve(detectMat(file.name))
            }
        };

        reader.onerror = () => {
            resolve("Erreur de lecture");
        };
    })
}

function detectMat(fileName) {
    var comboBox = document.querySelector('.matiere-select-base') 
    var options = comboBox.options;

    for (option in options) {
        if (options[option].innerText == "") {
            continue;
        }

        if (fileName.includes(options[option].innerText)) {
            return options[option].innerText;
        }
    }

    console.log("Pas trouvé")
}

// Boutton
function fileInputHandler(event) {
     showUploadedFiles(event.target.files)
}

// Zone de drop
function dropHandler(event) {
    event.preventDefault();

    let files;
    if (event.dataTransfer.items) {JSON.stringify(bodyObject)
        files = [...event.dataTransfer.items].map(item => item.getAsFile());
    } else {
        files = [...event.dataTransfer.files];
    }
    
    showUploadedFiles(files);
}

function showUploadedFiles(files) {
    document.getElementById("drop_zone").style.display = "none";
    document.getElementById("file_table").style.display = "block";

    let option = document.querySelector(".matiere-select-base");
    let body = document.getElementById("file_table_body");

    for (let i = 0; i < files.length; i++) {
        loadedFiles.push(files[i])

        let tr = document.createElement("tr");
        
        // File name
        let nameTd = document.createElement("td");
        nameTd.innerText = files[i].name;

        // File Type
        let typeTd = document.createElement("td");
        detectFileType(files[i]).then((type) => {
            if (type === "bilan") {
                typeTd.innerText = "Bilan";
            } else {
                let optpionClone = option.cloneNode(true);
                optpionClone.value = detectMat(files[i].name)
                typeTd.appendChild(optpionClone);
                optpionClone.style.display = "block";
            }
        })
        
        tr.appendChild(nameTd);
        tr.appendChild(typeTd);
        body.appendChild(tr);
    }
}

function submitFiles() {
    table = document.getElementById("file_table")
    rows = table.querySelectorAll("tr")

    for (i = 1; i < rows.length; i++) { // i = 1 pour skip le header
        
    }
}

function uploadFile(file, url, mat=null) {
    let formData = new FormData();
    formData.append('file', file);

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
            
            // Mise à jour des classes pour le triangle
            this.classList.toggle('asc', isAsc);
            this.classList.toggle('desc', !isAsc);
            
            // Mise à jour de l'attribut data-sort (si nécessaire)
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