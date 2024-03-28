setTimeout(function () {
    let messages = document.querySelector('.alert');
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 5000);