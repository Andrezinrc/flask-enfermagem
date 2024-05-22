$(document).ready(function() {
    $('#terminologia').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '/sugerir_terminologia',
                data: { q: request.term },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2
    });
});