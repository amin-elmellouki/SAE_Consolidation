var loadedFiles;

function autoSetMat() {
    var comboBox = document.getElementById('matiere-select'); 
    var options = comboBox.options;

    console.log(loadedFiles);
    for (let file of loadedFiles) {
        for (let option of options) {
            if (option.innerText.trim() === "") {
                continue;
            }
            if (file.name.includes(option.innerText)) {
                console.log(option);
                comboBox.value = option.value;
                return;
            }
        }
    }
    console.log("Pas trouvé");
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
        files = Array.from(ev.dataTransfer.items).map(item => item.getAsFile());
    } else {
        files = Array.from(ev.dataTransfer.files);
    }
    
    console.log(type);
    if (type === 'bilan') {
        uploadFiles(files, loadBilanUrl);
    } else {
        loadedFiles = files;
        autoSetMat();
    }
}

function uploadFiles(files, url, mat = null) {
    let formData = new FormData();
    let totalSize = 0;
    for (let file of files) {
        formData.append('files', file);
        totalSize += file.size;
    }
    if (mat) {
        formData.append('matiere', mat);
    }

    const simulatedSpeed = 10e6; 
    let estimatedTime = totalSize / simulatedSpeed * 1000;

    if (estimatedTime < 2000) {
        estimatedTime = 2000;
    }
    
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

    const progressBar = document.getElementById((url === loadBilanUrl) ? "progress-bar-bilan" : "progress-bar-qcm");
    progressBar.style.display = "block";
    const progressElement = progressBar.querySelector(".progress");

    let startTime = Date.now();
    let simulationInterval = setInterval(() => {
        let elapsed = Date.now() - startTime;
        let simulatedProgress = Math.min((elapsed / estimatedTime) * 100, 99);
        progressElement.style.width = simulatedProgress + "%";
        if (simulatedProgress >= 99) {
            clearInterval(simulationInterval);
        }
    }, 100);

    xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
            const realProgress = (event.loaded / event.total) * 100;
            if (realProgress > parseFloat(progressElement.style.width)) {
                progressElement.style.width = realProgress + "%";
            }
        }
    };

    xhr.onload = function () {
        clearInterval(simulationInterval);
        progressElement.style.width = "100%";
        if (xhr.status === 200) {
            console.log("Files uploaded successfully.");
            showMessage((url === loadBilanUrl) ? "bilan" : "qcm", false);
        } else {
            console.error("File upload failed.");
            showMessage((url === loadBilanUrl) ? "bilan" : "qcm", true);
        }
    };

    xhr.onerror = function () {
        clearInterval(simulationInterval);
        console.error("Error:", xhr.statusText);
        showMessage((url === loadBilanUrl) ? "bilan" : "qcm", true);
    };

    xhr.send(formData);
}

function showMessage(type, err) {
    document.getElementById(`${err ? "err" : "succ"}-${type}`).style.display = 'flex';
    setTimeout(() => {
        location.reload();
    }, 3000);
}

function sendQcm() {
    var e = document.getElementById('matiere-select');
    uploadFiles(loadedFiles, loadQcmUrl, e.options[e.selectedIndex].text);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
