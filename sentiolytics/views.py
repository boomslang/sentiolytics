import json
from locale import str, atoi
from multiprocessing.dummy import dict, list
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.db import connection, transaction
from django.utils import simplejson


def my_custom_sql():
    cursor = connection.cursor()
#    # Data modifying operation - commit required
#    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
#    transaction.commit_unless_managed()

    # Data modifying operation - commit required
#    cursor.execute("UPDATE django_site SET name = 'murat.com'  WHERE domain = 'example.com'")
#    cursor.execute("INSERT INTO django_site(name,domain) VALUES('meccid.com', 'mahir.com')")
#    transaction.commit_unless_managed()

    # Data retrieval operation - no commit required

    cursor.execute("SELECT * FROM sentiosp_drupal6.td_player")
    row = cursor.fetchall()

    return row

def test(request):
    sql_result = my_custom_sql()
#    sql_result = "textasd"
    d = dict(user = request.user, result = sql_result)
    return render_to_response("test.html", d)


def my_ajax_view(request):
#    if not request.is_ajax():
#        raise Http404
    if request.is_ajax():
        data_dict = dict(returnValue = request.GET.get('sendValue'))

        return HttpResponse(simplejson.dumps(data_dict), mimetype='application/json')
#
#def leaflet_view(request):
#    return render_to_response("test_leaflet.html")

#def my_ajax_view(request):
#    """returns json response"""
#    return HttpResponse(json.dumps({'foo': 'bar'}), mimetype='application/json')

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

#    match_id = 17
#    teams = get_teams(match_id)
#
#    rosters = [None,None]
#
#    rosters[0] = get_match_roster(match_id, teams[0][0])
#    rosters[1] = get_match_roster(match_id, teams[0][1])
#
#
#    players = [list(),list()]
#    for i in range(len(rosters)):
#        for element in rosters[i]:
#            name_string = element[1][0] + ". " + element[2]
#            players[i].append((name_string,element[3]))

    # TODO: Buradan sonrasi degisecek. Players list'indeki data ile doldur.

    data = load_match_roster_with_id(17)
    data_dict = dict((y, x) for x, y in data)

    team_1_id = data_dict.values()[0]
    sql_strings = ["", ""]
    for key, value in data_dict.iteritems():
        if value == team_1_id:
            sql_strings[0] += " PLAYER_ID = " + str(key) + " OR"
        else:
            sql_strings[1] += " PLAYER_ID = " + str(key) + " OR"

    team_players = list()
    cursor = connection.cursor()
    sql_string_base = "SELECT PLAYER_FULL_NAME, PLAYER_ID FROM sentiosp_drupal6.td_player WHERE "
    for sql_string in sql_strings:
        sql_string = sql_string_base + sql_string + " FALSE"
        cursor.execute(sql_string)

        data = cursor.fetchall()
        data_list = list()

        for element in data:
            element_list = list(element)
            element_list[0] = element[0].title()
            data_list.append(element_list)

        team_players.append(data_list)

#    cursor.callproc("CALL SP_GET_TEAM_PLAYERS",(1,1))

    return HttpResponse(simplejson.dumps(team_players), mimetype='application/json')

def update_chart(request):
    if not request.is_ajax():
        raise Http404

    player_ids = request.GET.getlist('sendValue[]')
    sql_string = "SELECT PLAYER_FULL_NAME, PLAYER_ID FROM sentiosp_drupal6.td_player WHERE "
    for id in player_ids:
        sql_string += " PLAYER_ID = " + id + " OR"
    sql_string += " FALSE"

#    print sql_string

    cursor = connection.cursor()
    cursor.execute(sql_string)
    data = cursor.fetchall()

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