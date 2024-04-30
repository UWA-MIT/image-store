$(document).ready(function () {
    $('form').on('submit', function () {
        disableSubmitBtn(true);
    });
    const generateForm = $('#generateForm');
    const generateModal = $('#generateModal');
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
                generateModal.modal('hide');
                overlay.hide();
                disableSubmitBtn(false);
                renderImage($('.products'), response.data);
            },
            error: function (xhr, status, error) {
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    alertInfo(xhr.responseJSON.message);
                } else {
                    alertInfo(error);
                }
                generateModal.modal('hide');
                overlay.hide();
                disableSubmitBtn(false);
            }
        });
    });
  $('.counter span').each(function() {
    const $span = $(this);
    const count = $span.data('count');
    $({ counter: 0 }).animate({ counter: count }, {
      duration: 1000,
      step: function() {
        $span.css('--num', Math.ceil(this.counter));
      }
    });
  });

  // Implement clear search function when clicking on clear x icon
    const searchInput = document.getElementById('nav-search-input');

    // Add an input event listener
    searchInput.addEventListener('input', function(event) {
        // Check if the input value is empty
        if (event.target.value === '') {
            $(searchInput).parent('form').submit()
        }
    });


    $('.latest-images-carousel').slick({
        dots: true,
        infinite: false,
        autoplay: true,
        speed: 300,
        slidesToShow: 4,
        slidesToScroll: 4,
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: true
                }
            }
        ]
    });
    hideAlert(5000);
    disableSubmitBtn(false)
    $(window).on('pageshow', function(event) {
        if (event.originalEvent.persisted) {
            window.location.reload();
        }
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
    const url = id + '/buy';
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
            if (xhr.responseJSON && xhr.responseJSON.message) {
                alertInfo(xhr.responseJSON.message);
            } else {
                alertInfo(error);
            }
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
    $('.base').prepend('<div class="alert alert-info alert-auto-disappear" role="alert" id="alert">' + message + '</div>');
    hideAlert(5000);
}

function hideAlert(time){
    setTimeout(function() {
        $('.alert-auto-disappear').fadeOut('slow', function() {
            $(this).remove();
        });
    }, time);
}

function disableSubmitBtn(disable) {
    const submit = $('#submit');
    submit.prop('disabled', disable);
    if(disable) {
        submit.text('Loading...');
    } else {
        submit.text(submit.data('text'));
    }
}