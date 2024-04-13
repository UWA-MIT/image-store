$(document).ready(function () {
    $('form').on('submit', function () {
        const submit = $('#submit');
        submit.prop('disabled', true);
        submit.text('Loading...');
    });
    const generateForm = $('#generateModal');
    const overlay = $('#overlay');
    generateForm.on('submit', function (e) {
        e.preventDefault();
        overlay.show();
        var url = '/products/generate_product';
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: $('#name').val().trim(),
                category: $('#category').val().trim(),
                price: $('#price').val().trim()
            }),
            success: function (response) {
                generateForm.trigger("reset");
                generateForm.modal('hide');
                overlay.hide();
                renderImage($('.products'), response.data);
            },
            error: function (xhr, status, error) {
                alertInfo(error);
                generateForm.modal('hide');
                overlay.hide();
            }
        });
    });
});

function transferDataToModal(elem) {
    const id = elem.getAttribute('data-id');
    const name = elem.getAttribute('data-name');
    const price = elem.getAttribute('data-price');
    document.getElementById('nameImage').innerText = name;
    document.getElementById('priceImage').innerText = '$' + price;
    const confirmButton = document.querySelector('button[onclick^="buyImage"]');
    confirmButton.setAttribute('onclick', `buyImage('${id}')`);
}

function buyImage(id) {
    var url = id + '/buy';
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            alertInfo(response.message);
            if (response.success) {
                $('[data-id="' + id + '"].card.area').remove();
            }
            $('#buyModal').modal('hide');
        },
        error: function (xhr, status, error) {
            alertInfo(error);
            $('#buyModal').modal('hide');
        }
    });
}

function renderImage(obj, data) {
    $(obj).prepend(`<div data-id="${data.id}" class="card area new">
            <img alt="${data.name}" class="card-img-top" src="/static/images/nft/${data.image}">
            <div class="card-body">
                <h6 class="card-title">${data.name} <span class="category">(${data.category})</span></h6>
                <p class="card-text">
                    <small class="price">$${data.price}</small> •
                    <small>${data.timestamp}</small>
                </p>
            </div>
            <div class="card-footer">
                <div class="row align-items-center g-2">
                    <div class="col-auto">
                        <img src="${data.avatar}" class="rounded-circle avatar-xs" alt="avatar">
                    </div>
                    <div class="col-auto">
                        <span>${data.username}</span>
                    </div>
                </div>
            </div>
        </div>`);
}

function alertInfo(message) {
    $('.base').prepend('<div class="alert alert-info" role="alert">' + message + '</div>');
}