from urllib import request
import pymysql
from django.http import JsonResponse

def root(request):
    return JsonResponse({'Message': 'Hello, welcome to my API.'})

def weather(request):
    con = pymysql.connect(host='localhost',
                            user='root',
                            password='test1234',
                            autocommit=True,
                            local_infile=1)
    cursor = con.cursor()
    date = request.GET.get('date')
    location = request.GET.get('location')
    trunc_sql = f"select * from coding_exercise.weather where date = '{date}' and location_id = '{location}'"
    cursor.execute(trunc_sql)
    data = cursor.fetchall()
    resp = {'max tempurature': data[0][1], 'min tempurature': data[0][2], 'precipitation': data[0][3]}
    return JsonResponse(resp)

def yld(request):
    con = pymysql.connect(host='localhost',
                            user='root',
                            password='test1234',
                            autocommit=True,
                            local_infile=1)
    cursor = con.cursor()
    year = request.GET.get('year')
    trunc_sql = f"select * from coding_exercise.yield where year = '{year}'"
    cursor.execute(trunc_sql)
    data = cursor.fetchall()
    resp = {'yield': data[0][1]}
    return JsonResponse(resp)

def weather_stats(request):
    con = pymysql.connect(host='localhost',
                            user='root',
                            password='test1234',
                            autocommit=True,
                            local_infile=1)
    cursor = con.cursor()
    year = request.GET.get('year')
    location = request.GET.get('location')
    trunc_sql = f"select * from coding_exercise.weather_stats where year = '{year}' and location_id = '{location}'"
    cursor.execute(trunc_sql)
    data = cursor.fetchall()
    resp = {'Message': 'Data not available'}
    if len(data)>0:
        resp = {'max tempurature': data[0][2], 'min tempurature': data[0][3], 'Avg precipitation': data[0][4]}
    return JsonResponse(resp)