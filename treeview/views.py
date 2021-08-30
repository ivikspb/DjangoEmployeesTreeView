import json
import os.path
import random
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Department, Employee


def treeview(request):
    return render(request, 'treeview/treeview.html')


def treeview_api(request, dip=None):
    if dip is None:
        return treeview_root(request)
    departments = Department.objects.filter(parent=dip)
    result = {}
    if departments.count() > 0:
        result['departments'] = []
        for department in departments:
            result['departments'].append(
                {'id': department.id, 'name': department.name}
            )
    try:
        employees = Employee.objects.filter(department=Department.objects.get(id=dip)).order_by('name')
    except Department.DoesNotExist:
        employees = None
    if employees is not None and employees.count() > 0:
        result['employees'] = []
        for employee in employees:
            result['employees'].append({'id': employee.id, 'name': employee.name})
    return HttpResponse(json.dumps(result), content_type="application/json")


def treeview_api_detal(request, eip):
    try:
        detal = Employee.objects.get(id=eip)
    except Employee.DoesNotExist:
        detal = None
    result = {}
    if detal is not None:
        result['detal'] = [f'ФИО: {detal.name}', f'Должность: {detal.position}',
                           f'Дата приема на работу: {detal.hired_date.strftime("%d.%m.%Y")}',
                           'Размер заработной платы: {:,}'.format(detal.salary)]
    return HttpResponse(json.dumps(result), content_type="application/json")

def treeview_root(request):
    departments = Department.objects.filter(level=0)
    result = {}
    if departments.count() > 0:
        result['departments'] = []
        for department in departments:
            result['departments'].append({'id': department.id, 'name': department.name, 'child': not department.is_leaf_node()})
    return HttpResponse(json.dumps(result), content_type="application/json")


def treeview_load_all(request):
    departments = Department.objects.all()
    employees = Employee.objects.all()
    employees_dict = {}
    for employee in employees:
        employees_dict.setdefault(employee.department.id, []).append(employee)

    return render(request, 'treeview/treeview-loadall.html', {'departments': departments, 'employees': employees_dict})


def genemployees(request):
    class GenFIO():
        def loadfile(self, filename):
            path = os.path.dirname(__file__)
            f = open(os.path.join(path, filename), 'r', encoding="utf-8")
            data = f.read()
            f.close()
            return data.split()

        def __init__(self):
            self.familynames = self.loadfile('familynames.txt')
            self.mannames = self.loadfile('mannames.txt')
            self.womannames = self.loadfile('womannames.txt')
            self.manmnames = self.loadfile('manmnames.txt')
            self.womanmnames = self.loadfile('womanmnames.txt')

        def genname(self):
            if random.random() > 0.5:
                return ' '.join((random.choice(self.familynames),
                                random.choice(self.mannames),
                                random.choice(self.manmnames)))
            else:
                return ' '.join((random.choice(self.familynames)+'а',
                                random.choice(self.womannames),
                                random.choice(self.womanmnames)))

    emps = Employee.objects.all()
    if emps.count() > 0:
        return redirect('treeview')
    departments = Department.objects.all()
    f = GenFIO()
    random_date = datetime(2010, 1, 1) + timedelta(days=random.randint(0, (datetime.now() -
                                                                           datetime(2010, 1, 1)).days))
    for i in range(50000):
        e = Employee(name=f.genname(), position='Должность '+str(i+1), hired_date=random_date,
                     salary=random.randint(2, 50) * 10000,
                     department=Department.objects.get(id=random.choice(departments).id))
        e.save()
    return redirect('treeview')
