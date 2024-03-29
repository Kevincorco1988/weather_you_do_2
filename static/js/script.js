setTimeout(function () {
    let messages = document.querySelector('.alert');
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 5000);

document.getElementById('id_city_name').disabled = true;