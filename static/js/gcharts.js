// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

//// Set a callback to run when the Google Visualization API is loaded.
//google.setOnLoadCallback(drawChart);


$(document).ready(function(){
    loadPlayers();
    fillDrawChart([]);
//    $('#Slider1').slider().onstatechange(function(){
//        update_chart();
//    });
});

//jQuery("#Slider1").slider({
//    from: 0,
//    to: 90,
//    step: 1,
//    smooth: true,
//    round: 0,
//    dimension: "",
//    skin: "plastic"
////    onstatechange: function() {
////        update_chart();
////    }
//});

//function fillChart(){
//    $.get("/gcharts_test/",{ sendValue: 'osman' },
//        function(data){
//            fillDrawChart(data);
//        }, "json");
//
//}
function fillDrawChart(returned_data) {
    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Player');
    data.addColumn('number', 'Distance');


    data.addRows(returned_data);
    // Set chart options
    var options = {'title':'Distance',
        'width':400,
        'height':300};

// Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}
function loadPlayers(){ // TODO: Checkbox bilgilerini doldur
    $.get("/load_players/",{ /*sendValue: str*/ },
        function(data){
//            $('#check_all').append(
//                $("<input/>")
//                    .attr("type", "checkbox")//of type checkbox
//                    .attr("class", "check_all")// with given name
//                    .attr("checked", false)// checked="checked" or checked=""
//                    .attr("id", $(this).attr('id')+"_")
////                    .attr("value", data[j][i][1])
//            );

            for(var j = 0; j < 2; j++)
            {
                for(var i = 0; i < data[j].length; i++)
                {
                    $("#players_team"+(j+1))
                        .append(
                        $("<input/>")
                            .attr("type", "checkbox")//of type checkbox
                            .attr("class", "player_cb"+(j+1))// with given name
                            .attr("checked", false)// checked="checked" or checked=""
                            .attr("name", "player")
                            .attr("team", data[2][j]) // TODO: Team id'leri gonderilen array'e [2] olarak ekle. checkbox'lara attr olarak eklemeye calis
                            .attr("value", data[j][i][1])
                        )
                        .append('<label> ' + data[j][i][0] + '</label><br>');
                }

                $('.player_cb'+(j+1)).click(function()    {
                    update_chart();
                });
            }
            $('.check_all').click(
                function()
                {
                    $("INPUT[class='player_" + $(this).attr('id') + "']").attr('checked', $(this).is(':checked'));
                    update_chart()
                }
            );
        }, "json");

}
function update_chart(){
    var data_to_send = [];

    data_to_send.push($("#Slider1").slider('value'));

//    $('.player_checkbox').each(function(i, obj) {
//        if( obj.is(':checked') == true )
//        {
//            alert(player_ids);
//            player_ids.push($('this').attr('name'));
//        }
//    });
    $('input[name="player"]:checked').each(function(){
        data_to_send.push($(this).attr('team') + '-' + $(this).attr('value') );
    });
//    alert(player_ids);
//    $.get("/ajax_update_chart/",{ sendValue: player_ids },
//        function(data){
//
////            fillDrawChart(data);
//        }, "json");
    $.ajax({
        url: '/ajax_update_chart/',
        type: 'GET',
        data: {sendValue:data_to_send},
        success: function(data){
            fillDrawChart(data)
        },
        dataType: 'json'
    });
}
