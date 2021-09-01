$(document).ready(function() {
    $('#confirm').click(function(e) {
        e.preventDefault();
        const def = document.getElementById("alt_definition").innerHTML;
        data_ = {w: "{{word}}", d: def };
        $.ajax({
            url: '/path',
            data: data_,
            type: 'POST',
            dataType: 'json',
            success: function(response) {
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
        console.log("{{word}}" + def);
        window.open('/finish');
    });
});