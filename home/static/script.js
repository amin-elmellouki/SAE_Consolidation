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

function fileInputHandler(event) {
     showUploadedFiles(event.target.files)
}

function dropHandler(event) {
    event.preventDefault();

    let files;
    if (event.dataTransfer.items) {
        files = [...event.dataTransfer.items].map(item => item.getAsFile());
    } else {
        files = [...event.dataTransfer.files];
    }
    
    showUploadedFiles(files);
}

function showUploadedFiles(files) {
    document.getElementById("drop_zone").style.display = "none";
    document.getElementById("file_table").style.display = "block";
    document.getElementById("upload_button").style.display = "flex";


    let option = document.querySelector(".matiere-select-base");
    let body = document.getElementById("file_table_body");

    for (let i = 0; i < files.length; i++) {
        loadedFiles.push(files[i])

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
        
        tr.appendChild(nameTd);
        tr.appendChild(typeTd);
        body.appendChild(tr);
    }
}

function submitFiles() {
    table = document.getElementById("file_table")
    rows = table.querySelectorAll("tr")

    for (i = 1; i < rows.length; i++) { // i = 1 pour skip le header
        console.log(rows[i])
        option = rows[i].querySelector("select")

        console.log(option)
        if (option) {
            console.log("Upload QCM")
            uploadFile(loadedFiles[i-1], loadQcmUrl, option.value)
        } else {
            console.log("Upload Bilan")
            uploadFile(loadedFiles[i-1], loadBilanUrl)
        }
    }
}

function uploadFile(file, url, mat=null) {
    let formData = new FormData();
    formData.append('file', file);

    let loading = document.getElementById("loading")

    console.log(mat)
    if (mat) {
        console.log("Ajout de matiere dans le formulaire")
        formData.append('matiere', mat)
    }

    loading.style.display = "flex"
    fetch(url, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
    }).then(response => {
        loading.style.display = "none"

        if (response.ok) {
            console.log("Files uploaded successfully.");
            showMessage(false)
        } else {
            console.error("File upload failed.");
            showMessage(true)
        }
    }).catch(error => {
        console.error("Error:", error);
        showMessage(true)
    });
}

function showMessage(err) {
    document.getElementById(`${(err) ? ("err") : ("succ")}`).style.display = 'flex';
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
    const weekButton = document.querySelector('.aside-button');
    if (weekButton) {
      let isAsc = false;
      weekButton.addEventListener('click', function() {
        isAsc = !isAsc;
        this.classList.toggle('asc', isAsc);
        this.classList.toggle('desc', !isAsc);
        this.setAttribute('data-sort', isAsc ? 'asc' : 'desc');
        
        const scrollable = document.querySelector('.aside-scrollable');
        const weekElements = Array.from(scrollable.querySelectorAll('.week'));
        
        weekElements.sort((a, b) => {
          const getDateText = (element) => {
            const dateLink = element.querySelector('a:first-child');
            return dateLink.textContent.trim().split('(')[0].trim();
          };
          
          const aDateText = getDateText(a);
          const bDateText = getDateText(b);
          
          return isAsc ? aDateText.localeCompare(bDateText) : bDateText.localeCompare(aDateText);
        });
        
        scrollable.innerHTML = '';
        weekElements.forEach(weekElement => scrollable.appendChild(weekElement));
      });
    }
});
