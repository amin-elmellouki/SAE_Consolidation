document.addEventListener("DOMContentLoaded", function () {
    const icone_affiche = "fa-eye";
    const icone_masque = "fa-eye-slash";
    const buttons = document.querySelectorAll(".toggle-password");

    // Ajoute un gestionnaire d'événements à chaque bouton
    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const passwordField = this.previousElementSibling;
            const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
            passwordField.setAttribute("type", type);

            // Basculer entre les icônes pour indiquer l'état actuel
            const icon = this.querySelector("i");
            if (type === "password") {
                icon.classList.remove(icone_masque);
                icon.classList.add(icone_affiche);
            } else {
                icon.classList.remove(icone_affiche);
                icon.classList.add(icone_masque);
            }
        });
    });
});
