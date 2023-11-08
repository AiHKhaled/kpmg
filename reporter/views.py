from django.shortcuts import render
from .models import Project, Task
from django.db.models import Sum
import csv
from django.http import HttpResponse
from django.db import connection



def getTableProjects(status_filter=None):

    base_query = """
        SELECT projects.id, projects.name, projects.status, 
        SUM(CASE WHEN tasks.status = 'To Do' THEN 1 ELSE 0 END) AS to_do,
        SUM(CASE WHEN tasks.status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
        SUM(CASE WHEN tasks.status = 'Done' THEN 1 ELSE 0 END) AS completed,
        SUM(CASE WHEN tasks.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled
        FROM reporter_project AS projects
        JOIN reporter_task AS tasks ON projects.id = tasks.project_id
        GROUP BY projects.id
    """
    if status_filter:
        sql_query = f"{base_query} WHERE tasks.status = %s"
        tableProjects = Project.objects.raw(sql_query, [status_filter])
    else:
        tableProjects = Project.objects.raw(base_query)

    return tableProjects

def data_view(request):
    
    totalProjects = Project.objects.count()
    activeProjects = Project.objects.filter(status='Active').count() 
    activeProjects  = str(activeProjects * 100 / totalProjects) + "%" 


    revenue = Project.objects.filter(status='Completed').aggregate(Sum('cost')) 
    monthly_revenue = Project.objects.raw(
        """
            SELECT id, SUM(cost) AS revenue
            FROM reporter_project
            WHERE status = 'Completed'
            AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now', '-1 month', 'localtime')

        """
    )


    # tableProjects =Project.objects.annotate(
    #     to_do=Sum(Case(When(tasks__status='To Do', then=1), default=0, output_field=models.IntegerField())),
    #     in_progress=Sum(Case(When(tasks__status='In Progress', then=1), default=0, output_field=models.IntegerField())),
    #     completed=Sum(Case(When(tasks__status='Done', then=1), default=0, output_field=models.IntegerField())),
    #     cancelled=Sum(Case(When(tasks__status='Cancelled', then=1), default=0, output_field=models.IntegerField()))
    # ).values('id', 'name', 'status', 'to_do', 'in_progress', 'completed', 'cancelled')

   
    return render(request, 'index.html', {
        'tableProjects': getTableProjects(),
        'projects':{
            'value': totalProjects,
            'subvalue': activeProjects, 
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

# views.py

def export_csv(request):
    status_filter = request.GET.getlist('status_filter')  # Use getlist to handle multiple selections

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


    # Construct a parameterized SQL query to accommodate multiple selections
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
    # sql_query = """
    #     SELECT projects.id, projects.name, projects.status, 
    #     SUM(CASE WHEN tasks.status = 'To Do' THEN 1 ELSE 0 END) AS to_do,
    #     SUM(CASE WHEN tasks.status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
    #     SUM(CASE WHEN tasks.status = 'Done' THEN 1 ELSE 0 END) AS completed,
    #     SUM(CASE WHEN tasks.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled
    #     FROM reporter_project AS projects
    #     JOIN reporter_task AS tasks ON projects.id = tasks.project_id
    #     WHERE tasks.status IN %s
    #     GROUP BY projects.id
    # """
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
