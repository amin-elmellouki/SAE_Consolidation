var loadedFiles;

function fileInputHandler(event, type) {
    const files = event.target.files;
    let url = type === 'bilan' ? loadBilanUrl : loadQcmUrl;
    uploadFiles(files, url);
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
    
    if (type === 'bilan') {
        uploadFiles(files, loadBilanUrl);
    } else {
        loadedFiles = files;
    }


function uploadFiles(files, url) {
    let formData = new FormData();
    for (let file of files) {
        formData.append('files', file);
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
        } else {
            console.error("File upload failed.");
        }
    }).catch(error => {
        console.error("Error:", error);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
