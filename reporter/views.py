from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
from django.db import connection
from django.core.paginator import Paginator

from .models import Project, Task
from .utils import get_project_stats
import csv


def data_view(request):
    
    page = request.GET.get('page', 1)
    items_per_page = 10

    stats = get_project_stats()  
    revenue = Project.objects.filter(status='Completed').aggregate(Sum('cost')) 
    monthly_revenue = Project.objects.raw(
        """
            SELECT id, SUM(cost) AS revenue
            FROM reporter_project
            WHERE status = 'Completed'
            AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now', '-1 month', 'localtime')

        """
    )

    tableProjects = Project.objects.raw(
        """
        SELECT projects.id, projects.name, projects.status, 
        SUM(CASE WHEN tasks.status = 'To Do' THEN 1 ELSE 0 END) AS to_do,
        SUM(CASE WHEN tasks.status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
        SUM(CASE WHEN tasks.status = 'Done' THEN 1 ELSE 0 END) AS completed,
        SUM(CASE WHEN tasks.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled
        FROM reporter_project AS projects
        JOIN reporter_task AS tasks ON projects.id = tasks.project_id
        GROUP BY projects.id
    """
    )
   

    paginator = Paginator(tableProjects, items_per_page)
    current_page_data = paginator.get_page(page)
   
    return render(request, 'index.html', {
        'tableProjects': current_page_data,
        'projects':{
            
            'value': stats['total'],
            'subvalue':str(stats['active'] * 100 / stats['total'] )+ "%", 
            "icon": "folder-open",
            "title": "Total Projects",
            "subtitle": "currently active"
        }, 
        "revenue":{
            "value":"$" + str(revenue['cost__sum']),
            "subvalue":"$" + str(monthly_revenue[0].revenue),
            "icon": "currency-dollar",
            "title": "Total Revenue",
            "subtitle": "from last month",
        },
        "tasks": {
            "value": "+" + str(Task.objects.filter(status='In Progress').count()),
            "subvalue": "+" + str(Task.objects.filter(status='Done').count()),
            "icon": "document-text",
            "title": "Tasks in progress",
            "subtitle": "completed",
        }
        
    })


def export_csv(request):
    status_filter = request.GET.getlist('status_filter') 

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tableProjects.csv"'

    writer = csv.writer(response)
    header = ['Project ID', 'Name', 'Status']

    if ('To Do' in status_filter):
        header.append('To Do')
    if ('In Progress' in status_filter):
        header.append('In Progress')
    if ('Done' in status_filter):
        header.append('Done')
    if ('Cancelled' in status_filter):
        header.append('Cancelled')
    if not status_filter:
       status_filter = ['To Do', 'In Progress', 'Done', 'Cancelled']
       header.extend(status_filter)

    writer.writerow(header)
    sql_query = f"""
        SELECT projects.id, projects.name, projects.status, 
        SUM(CASE WHEN tasks.status = 'To Do' THEN 1 ELSE 0 END) AS to_do,
        SUM(CASE WHEN tasks.status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
        SUM(CASE WHEN tasks.status = 'Done' THEN 1 ELSE 0 END) AS completed,
        SUM(CASE WHEN tasks.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled
        FROM reporter_project AS projects
        JOIN reporter_task AS tasks ON projects.id = tasks.project_id
        WHERE tasks.status IN ({', '.join(['%s']*len(status_filter))})
        GROUP BY projects.id
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_query, status_filter)
        results = cursor.fetchall()
        

    for row in results:
        values = [row[0], row[1], row[2]]
        if 'To Do' in status_filter:
            values.append(row[3])
        if 'In Progress' in status_filter:
            values.append(row[4])
        if 'Done' in status_filter:
            values.append(row[5])
        if 'Cancelled' in status_filter:
            values.append(row[6])
        writer.writerow(values)

    return response
