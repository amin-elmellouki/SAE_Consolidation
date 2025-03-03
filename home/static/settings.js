function confirmerViderBase() {
    if (confirm("Êtes-vous sûr de vouloir vider la base de données ? Cette action est irréversible.")) {
        document.getElementById('vider-form').submit();
    }
}

setTimeout(function() {
    var messages = document.querySelectorAll('.messages li');
    messages.forEach(function(message) {
        message.classList.add('hide');
    });

    setTimeout(function() {
        var messagesContainer = document.querySelector('.messages');
        if (messagesContainer) {
            messagesContainer.remove();
        }
    }, 1000);
}, 3000);