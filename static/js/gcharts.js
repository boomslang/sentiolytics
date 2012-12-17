// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

//// Set a callback to run when the Google Visualization API is loaded.
//google.setOnLoadCallback(drawChart);


$(document).ready(function(){
    loadPlayers();
//    fillChart();
});
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
    data.addColumn('string', 'Player');
    data.addColumn('number', 'Number');

    data.addRows(returned_data);
    // Set chart options
    var options = {'title':'Players',
        'width':400,
        'height':300};

// Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
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
    var player_ids = [];
//    $('.player_checkbox').each(function(i, obj) {
//        if( obj.is(':checked') == true )
//        {
//            alert(player_ids);
//            player_ids.push($('this').attr('name'));
//        }
//    });
    $('input[name="player"]:checked').each(function(){
        player_ids.push($(this).attr('value'));
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
        data: {sendValue:player_ids},
        success: function(data){
            fillDrawChart(data)
        },
        dataType: 'json'
    });
}
