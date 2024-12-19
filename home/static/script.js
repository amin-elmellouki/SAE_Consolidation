var loadedFiles;

function fileInputHandler(event, type) {
    const files = event.target.files;
    
    if (type === 'bilan') {
        uploadFiles(files, loadBilanUrl);
    } else {
        loadedFiles = files;
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
