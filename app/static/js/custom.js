$(document).ready(function() {
    $('form').on('submit', function() {
        const submit = $('#submit');
        submit.prop('disabled', true);
        submit.text('Loading...');
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
    success: function(response) {
      alertInfo(response.message);
      if(response.success){
          $('[data-id="' + id + '"].card.area').remove();
      }
      $('#buyModal').modal('hide');
    },
    error: function(xhr, status, error) {
      alertInfo(error);
      $('#buyModal').modal('hide');
    }
  });
}
function alertInfo(message){
    $('.base').prepend('<div class="alert alert-info" role="alert">' + message + '</div>');
}