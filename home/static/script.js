var loadedFiles;

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
        let tr = document.createElement("tr");
        
        let nameTd = document.createElement("td");
        nameTd.innerText = files[i].name;

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
        
        let deleteTd = document.createElement("td");
        deleteTd.innerText = "Le gros sexe a guigui";
        
        tr.appendChild(nameTd);
        tr.appendChild(typeTd);
        tr.appendChild(deleteTd);

        body.appendChild(tr);
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
