/**
 * This JavaScript file contains custom client-side code for BuySell web application.
 */

// Execute when the DOM is fully loaded
$(document).ready(function () {
    
    // Disable submit button on form submission
    $('form').on('submit', function () {
        disableSubmitBtn(true);
    });

    // Handle form submission for generating a product
    const generateForm = $('#generateForm');
    const generateModal = $('#generateModal');
    const overlay = $('#overlay');
    let balanceElement = $('#user-main-balance')

    
    generateForm.on('submit', function (e) {
        e.preventDefault();
        overlay.show();
        var url = '/products/generate_product';
        let money = parseInt(balanceElement.text().replace("$", ""));
        let image_generation_cost = parseInt($('.generate-image-reward-point').text().replace('$', ''));
        var newBalance = money - image_generation_cost;


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
                balanceElement.text('$' + newBalance)
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

    // Counter animation for each span element
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

    // Clear search function when clicking on clear icon
    const searchInput = document.getElementById('nav-search-input');
    searchInput.addEventListener('input', function(event) {
        if (event.target.value === '') {
            $(searchInput).parent('form').submit();
        }
    });

    // Configure slick carousel for latest images display
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

    // Hide alert after specified time
    hideAlert(5000);
    // Enable submit button
    disableSubmitBtn(false);

    // Reload page on pageshow event
    $(window).on('pageshow', function(event) {
        if (event.originalEvent.persisted) {
            window.location.reload();
        }
    });
});

// Function to transfer data to modal
function transferDataToModal(elem) {
    const id = elem.getAttribute('data-id');
    const name = elem.getAttribute('data-name');
    const price = elem.getAttribute('data-price');
    document.getElementById('nameImage').innerText = name;
    document.getElementById('priceImage').innerText = '$' + price;
    const confirmButton = document.querySelector('button[onclick^="buyImage"]');
    confirmButton.setAttribute('onclick', `buyImage('${id}')`);
}

// Function to handle buying an image
function buyImage(id) {
    const url = id + '/buy';
    let balanceElement = $('#user-main-balance')
    var money = parseInt(balanceElement.text().replace("$", ""));
    var price = parseInt($('[data-id="' + id + '"]').find('.price').text().replace('$', ''));
    var newBalance = money - price;

    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            balanceElement.text('$' + newBalance)

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

// Function to render an image
function renderImage(obj, data) {
    $(obj).prepend(`<div data-id="${data.id}" class="card area new">
            <img alt="${data.name}" class="card-img-top" src="/static/images/nft/${data.image}">
            <div class="card-body">
                <h6 class="card-title">` + truncate(data.name, 7) + ` <span class="category">(${data.category})</span></h6>
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

function truncate(string, maxLength) {
    if (string.length > maxLength) {
        return string.substring(0, maxLength) + "...";
    } else {
        return string;
    }
}

// Function to display alert message
function alertInfo(message) {
    $('.base').prepend('<div class="alert-message alert alert-info alert-auto-disappear" role="alert" id="alert">' + message + '</div>');
    hideAlert(5000);
}

// Function to hide alert after specified time
function hideAlert(time){
    setTimeout(function() {
        $('.alert-auto-disappear').fadeOut('slow', function() {
            $(this).remove();
        });
    }, time);
}

// Function to enable/disable submit button
function disableSubmitBtn(disable) {
    const submit = $('#submit');
    submit.prop('disabled', disable);
    if(disable) {
        submit.text('Loading...');
    } else {
        submit.text(submit.data('text'));
    }
}
