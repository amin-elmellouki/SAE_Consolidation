function dropHandler(ev, type) {
    console.log("File(s) dropped");
    
    ev.preventDefault();

    // Récupération des fichiers
    let files
    if (ev.dataTransfer.items) {
        files = [...ev.dataTransfer.items].map(item => item.getAsFile());
    } else {
        files = [...ev.dataTransfer.files];
    }
    
    // Choix de l'url
    let url;
    if (type === 'bilan') {
        url = loadBilanUrl;
    } else {
        url = loadQcmUrl
    }

    // Envoi
    let formData = new FormData();
    files.forEach((file, index) => {
        formData.append(`files`, file);
    });

    fetch(url, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
