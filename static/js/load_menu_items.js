$(document).ready(function(){
    $('.league_item').click(function()    {
        req_load_matches($(this).attr('id'));
    });
});

function req_load_matches(data_to_send)
{
    $.ajax({
        url: '/ajax_load_matches/',
        type: 'GET',
        data: {sendValue:data_to_send},
        success: function(data){
            load_matches(data)
        },
        dataType: 'json'
    });
}

function load_matches(data)
{
    $("#match_list").empty()
    for(var i = 0; i < data.length; i++)
    {
        $("#match_list")
            .append(
            $('<li>')
                .append(
                    $("<a>")
                        .attr("class", "match_item")// with given name
                        .attr("match_id", data[i][0])
                        .append(data[i][1] + " - " + data[i][2]
                    )
                )
                .click(
                    function()
                    {
                        $("#verticalmenu").css('visibility', 'visible');
                    }
                )
        );
    }
}
