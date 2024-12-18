/**
 * Script pour gérer la validation d'un formulaire de connexion.
 * Objectif : Empêcher la soumission du formulaire si les champs ne respectent pas
 * les contraintes de validation, tout en fournissant un retour visuel à l'utilisateur.
 */

document.addEventListener("DOMContentLoaded", function () {
    const usernameField = document.querySelector("input[name='username']");
    const passwordField = document.querySelector("input[name='password']");
    const globalErrorsContainer = document.getElementById("global-errors");
    const loginForm = document.getElementById("login-form");

    // Ajout dynamique d'un conteneur pour les erreurs spécifiques au champ mot de passe
    const passwordErrorMessage = document.createElement("div");
    passwordErrorMessage.className = "error-message hidden";
    passwordField.parentNode.appendChild(passwordErrorMessage);

    /**
     * Valide les règles de complexité du mot de passe.
     *
     * Contraintes :
     * - Longueur minimale : 8 caractères.
     * - Au moins une lettre majuscule, une lettre minuscule, un chiffre, et un caractère spécial.
     * - Pas d'espaces autorisés.
     *
     * @param {string} password - Le mot de passe à analyser.
     * @returns {string[]} - Liste des messages d'erreur si des règles sont violées.
     */
    const validatePassword = (password) => {
        const errors = [];
        if (password.length < 8) errors.push("Le mot de passe doit contenir au moins 8 caractères.");
        if (!/[A-Z]/.test(password)) errors.push("Le mot de passe doit contenir une lettre majuscule.");
        if (!/[a-z]/.test(password)) errors.push("Le mot de passe doit contenir une lettre minuscule.");
        if (!/\d/.test(password)) errors.push("Le mot de passe doit contenir un chiffre.");
        if (!/[!@#$%^&*(),.?\":{}|<>]/.test(password)) errors.push("Le mot de passe doit contenir un caractère spécial.");
        if (/\s/.test(password)) errors.push("Le mot de passe ne doit pas contenir d'espaces.");
        return errors;
    };

    /**
     * Gère l'affichage des erreurs pour un champ spécifique.
     *
     * Raison : Les erreurs sont affichées dynamiquement pour fournir un retour immédiat
     * sur les saisies incorrectes.
     *
     * @param {HTMLElement} element - Le champ HTML ciblé.
     * @param {HTMLElement} errorContainer - L'élément HTML où afficher les erreurs.
     * @param {string[]} errors - Liste des erreurs à afficher.
     */
    const displayErrors = (element, errorContainer, errors) => {
        if (errors.length > 0) {
            element.classList.add("invalid");
            errorContainer.classList.remove("hidden");
            errorContainer.innerHTML = errors.join("<br>");
        } else {
            element.classList.remove("invalid");
            errorContainer.classList.add("hidden");
            errorContainer.innerHTML = "";
        }
    };

    usernameField.addEventListener("input", () => {
        const username = usernameField.value.trim();
        const errors = username === "" ? ["Le champ nom d'utilisateur ne peut pas être vide."] : [];
        usernameField.setCustomValidity(errors.length > 0 ? errors[0] : "");
        usernameField.reportValidity();
    });

    passwordField.addEventListener("input", () => {
        const errors = validatePassword(passwordField.value);
        displayErrors(passwordField, passwordErrorMessage, errors);
    });

    // Gestion de la soumission du formulaire
    loginForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const username = usernameField.value.trim();
        const password = passwordField.value;

        const formErrors = [];
        if (username === "") formErrors.push("Le nom d'utilisateur ne peut pas être vide.");
        const passwordErrors = validatePassword(password);
        if (passwordErrors.length > 0) formErrors.push(...passwordErrors);

        displayErrors(globalErrorsContainer, globalErrorsContainer, formErrors);

        if (formErrors.length === 0) {
            globalErrorsContainer.classList.add("hidden");
            loginForm.submit();
        }
    });
});
