from django.shortcuts import render,HttpResponse
from . models import Employee,Role,Deparment
from datetime import datetime
from django.db.models import Q

def index(request):
    return render(request,"index.html")

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        "emps":emps
    }
    print(context)
    return render(request,"view_all_emp.html",context)



    # ///////////////// Add Employee //////////////////
def add_emp(request):
    if request.method == "POST":
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            salary = int(request.POST['salary'])
            bonus = int(request.POST['bonus'])
            phone = int(request.POST['phone'])
            dept_id = int(request.POST['dept'])
            role_id = int(request.POST['role'])

            # Check if the provided department and role IDs exist
            department = Deparment.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)

            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept=department,
                role=role,
                hire_date=datetime.now()
            )
            new_emp.save()

            return HttpResponse("Employee added Successfully")
        except Deparment.DoesNotExist:
            return HttpResponse("Error: Department with the provided ID does not exist.")
        except Role.DoesNotExist:
            return HttpResponse("Error: Role with the provided ID does not exist.")
        except Exception as e:
            return HttpResponse(f"An Exception Occurred! Employee has not been added. Error: {str(e)}")
    elif request.method == "GET":
        return render(request, "add_emp.html")
    else:
        return HttpResponse("Invalid request method")








        

    
# /////////Remove Employee///////////////////   

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employe Remove Successfully")
        except:
            return HttpResponse("Please Enter A valid Emp ID")
    emps = Employee.objects.all()
    context = {
        "emps" : emps
    }
    return render(request,"remove_emp.html",context)


# /////////////Filter Employee////////////////////////////////

def filter_emp(request):
    if request.method == "POST":
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept_name = dept)
        if role:
            emps = emps.filter(role_name = role)

        context ={
            "emps" : emps
        }

        return render(request,"view_all_emp.html",context) 
    
    elif request.method == "GET":
        return render(request,"filter_emp.html")
    else:
        return HttpResponse("An Exception Occuried")