$(document).ready(function() {
    $('#confirm').click(function(e) {
        e.preventDefault();
        const def = document.getElementById("alt_definition").innerHTML;
        const word = document.getElementById("confirm_word").innerHTML;
        data_ = {w: word, d: def };
        $.ajax({
            url: '/finish',
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
        console.log(word + ": " + def);
        //for some reason (get into that later) I cannot open this in a new tab?
        window.open('/finish');
    });
});