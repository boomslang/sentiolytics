import json
from locale import str, atoi
from multiprocessing.dummy import dict, list
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.db import connection, transaction
from django.utils import simplejson
from sentiolytics.models import Match_info

def test(request):
    d = dict(user = request.user, leagues = load_leagues())
    return render_to_response("test.html", d)


def my_ajax_view(request):
#    if not request.is_ajax():
#        raise Http404
    if request.is_ajax():
        data_dict = dict(returnValue = request.GET.get('sendValue'))

        return HttpResponse(simplejson.dumps(data_dict), mimetype='application/json')

def gcharts(request):
    if not request.is_ajax():
        raise Http404

    cursor = connection.cursor()
    cursor.execute("SELECT PLAYER_FULL_NAME, PLAYER_ID FROM sentiosp_drupal6.td_player LIMIT 0, 11")
    data = cursor.fetchall()
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def load_players(request): # TODO : Gereksiz fazla cagiriliyor olabilir, kontrol et.
    if not request.is_ajax():
        raise Http404

    match_id = 17
    match = Match_info(match_id = match_id)
    match.save()

    teams = get_teams(match_id)

    rosters = [None,None]

    rosters[0] = get_match_roster(match_id, teams[0][0])
    rosters[1] = get_match_roster(match_id, teams[0][1])


    players = [list(),list()]
    for i in range(len(rosters)):
        for element in rosters[i]:
            name_string = element[1][0] + ". " + element[2]
            players[i].append((name_string,element[3]))

    players.append(teams[0])
    # TODO: Buradan sonrasi degisecek. Players list'indeki data ile doldur.

#    data = load_match_roster_with_id(17)
#    data_dict = dict((y, x) for x, y in data)
#
#    team_1_id = data_dict.values()[0]
#    sql_strings = ["", ""]
#    for key, value in data_dict.iteritems():
#        if value == team_1_id:
#            sql_strings[0] += " PLAYER_ID = " + str(key) + " OR"
#        else:
#            sql_strings[1] += " PLAYER_ID = " + str(key) + " OR"
#
#    team_players = list()
#    cursor = connection.cursor()
#    sql_string_base = "SELECT PLAYER_FULL_NAME, PLAYER_ID FROM sentiosp_drupal6.td_player WHERE "
#    for sql_string in sql_strings:
#        sql_string = sql_string_base + sql_string + " FALSE"
#        cursor.execute(sql_string)
#
#        data = cursor.fetchall()
#        data_list = list()
#
#        for element in data:
#            element_list = list(element)
#            element_list[0] = element[0].title()
#            data_list.append(element_list)
#
#        team_players.append(data_list)

    return HttpResponse(simplejson.dumps(players), mimetype='application/json')
#    return HttpResponse(simplejson.dumps(team_players), mimetype='application/json')

def update_chart(request):
    if not request.is_ajax():
        raise Http404

    player_info_str = request.GET.getlist('sendValue[]')
    slider_values = player_info_str.pop(0).split(';')

    player_info = (player.split('-') for player in player_info_str) # Team_id , jersey_num

    match_id = Match_info.objects.all().reverse()[0].match_id # Latest match id

#    match_min_lower = '0'
#    match_min_upper = '90'

    match_min_lower = slider_values[0]
    match_min_upper = slider_values[1]

    data = list()

    if(len(player_info_str)):
        sql_string_base = "SELECT JERSEY_NUMBER, SUM(DISTANCE) FROM sentiosp_drupal6.tf_match_stats_processed WHERE MATCH_ID = "\
                    + str(match_id) + " AND MATCH_MINUTE <= " + match_min_upper \
                     + " AND MATCH_MINUTE >= " + match_min_lower
        cursor = connection.cursor()
        for player in player_info:
            sql_string = sql_string_base + " AND JERSEY_NUMBER = " + player[1] + " AND TEAM_ID = " + player[0]
            cursor.execute(sql_string)
            returned_data =  cursor.fetchone()
            if returned_data[0] is not None and returned_data[1] is not None:
                data.append(returned_data)

            print 'test'

#        for player in player_info:
#            sql_string += "( JERSEY_NUMBER = " + player[1] + " AND TEAM_ID = " + player[0] + " ) OR "
#        sql_string += "FALSE )"
#        cursor.execute(sql_string)
#        returned_data =  cursor.fetchall()

#    player_ids = request.GET.getlist('sendValue[]')
#    sql_string = "SELECT PLAYER_FULL_NAME, PLAYER_ID FROM sentiosp_drupal6.td_player WHERE "
#    for id in player_ids:
#        sql_string += " PLAYER_ID = " + id + " OR"
#    sql_string += " FALSE"

#    print sql_string

#    cursor = connection.cursor()
#    cursor.execute(sql_string)
#    data = cursor.fetchall()

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def load_match_roster_with_id(id):

    sql_string = "SELECT TEAM_ID, PLAYER_ID FROM sentiosp_drupal6.tf_match_roster WHERE MATCH_ID = " + str(id)

#    print sql_string

    cursor = connection.cursor()
    cursor.execute(sql_string)
    data = cursor.fetchall()

    return data

def get_match_roster(match_id, team_id):
    sql_string = "CALL sentiosp_drupal6.SP_GET_MATCH_ROSTER ("+ str(match_id)  +","+ str(team_id) +");"
    print sql_string
    cursor = connection.cursor()
    cursor.execute(sql_string)
    data = cursor.fetchall()
    return data

def get_teams(match_id):

    sql_string = "SELECT HOME_TEAM_ID, VISITOR_TEAM_ID FROM sentiosp_drupal6.tf_match WHERE MATCH_ID = " + str(match_id)

    #    print sql_string
    cursor = connection.cursor()
    cursor.execute(sql_string)
    data = cursor.fetchall()

    return data

def load_leagues():
    sql_string = "SELECT LEAGUE_ID, LEAGUE_NAME FROM sentiosp_drupal6.td_league;"
    cursor = connection.cursor()
    cursor.execute(sql_string)
    data = cursor.fetchall()
#    data_list = list({id: x, name: y} for x, y in data)
    return data

def ajax_load_matches(request):
    if not request.is_ajax():
        raise Http404

    league_id = request.GET.get('sendValue')

    sql_string = "SELECT MATCH_ID, HOME_TEAM_ID, VISITOR_TEAM_ID FROM sentiosp_drupal6.tf_match WHERE MATCH_LEAGUE_ID =" + league_id + ";"
    cursor = connection.cursor()
    cursor.execute(sql_string)
    matches = cursor.fetchall()

    home_team_ids = list(match[1] for match in matches)
    away_team_ids = list(match[2] for match in matches)
    team_ids = list(set(home_team_ids + away_team_ids))

    sql_string = "SELECT TEAM_ID, TEAM_NAME FROM sentiosp_drupal6.td_team WHERE "

    for team_id in team_ids:
        sql_string += " TEAM_ID = " + str(team_id) + " OR"

    sql_string += " FALSE"
    cursor = connection.cursor()
    cursor.execute(sql_string)
    returned_data = cursor.fetchall()
    team_names = dict(returned_data)

    data = list()

    for match in matches:
        try:
            data.append((match[0], team_names[match[1]], team_names[match[2]] ))
        except:
            print match
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
