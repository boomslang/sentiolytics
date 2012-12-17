$(document).ready(function(){
    $('#txtValue').keyup(function(){
        sendValue($(this).val());

    });
});
function sendValue(str){
    $.get("/ajax_test/",{ sendValue: str },
        function(data){
            $('#display').html(data.returnValue);
        }, "json");

}

