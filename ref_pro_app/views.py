from django.shortcuts import render, redirect, HttpResponse
from ref_pro_app.models import Contact, Students, Withdraw
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
def index(request):
    return render(request, "index.html")

def profile(request):
    return render(request, "criteria.html")

def faq(request):
    return render(request, "faq.html")

def privacypolicy(request):
    return render(request, "privacypolicy.html")

def referralguidelines(request):
    return render(request, "referralguidelines.html")

def contact(request):
    if request.method == "POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request, "We will get back to you soon...")


    return render(request, "contact.html")

def refer(request):
    if request.method == "POST":
        name=request.POST.get("name")
        pnumber=request.POST.get("pnumber")
        pnumber2=request.POST.get("pnumber2")
        course=request.POST.get("course")
        email=request.POST.get("email")
        status=request.POST.get("status")
        remarks=request.POST.get("remarks")
    
        myquery=Students(name=name, phonenumber=pnumber, alternatenumber=pnumber2, course=course, email=email, status=status, remarks=remarks )
        myquery.save()
        messages.info(request, "Your friend has been registered.")

    return render(request, "refer.html")



def about(request):
    return render(request, "about.html")


# Check if user is an admin
def is_admin(user):
    return user.is_superuser

# Check if user is staff
def is_staff(user):
    return user.is_staff


# Admin Portal Functions

@login_required
@user_passes_test(is_admin)
def adminportal(request):
    ref = Students.objects.all()

    context = {
        "ref":ref,
               }
    return render(request, "adminportal.html", context)

def add(request):
    if request.method == "POST":
        name=request.POST.get("name")
        pnumber=request.POST.get("pnumber")
        pnumber2=request.POST.get("pnumber2")
        course=request.POST.get("course")
        email=request.POST.get("email")
        remarks=request.POST.get("remarks")
        referer=request.POST.get("referer")
        status=request.POST.get("status")

        myquery=Students(name=name, phonenumber=pnumber, alternatenumber=pnumber2, course=course, email=email, remarks=remarks, status=status, referer=referer )
        myquery.save()
        #messages.info(request, "New Candidate Added.")
        return redirect('adminportal')
    
    return render(request, "adminportal.html")

def edit(request):
    ref = Students.objects.all()

    context = {
        "ref":ref,
               }
    return render(request, "adminportal.html", context)

def update(request, id):
    if request.method == "POST":
        name=request.POST.get("name")
        pnumber=request.POST.get("pnumber")
        pnumber2=request.POST.get("pnumber2")
        course=request.POST.get("course")
        email=request.POST.get("email")
        remarks=request.POST.get("remarks")
        referer=request.POST.get("referer")
        status=request.POST.get("status")
        

        myquery=Students(id=id, name=name, phonenumber=pnumber, alternatenumber=pnumber2, course=course, email=email, status=status, remarks=remarks, referer=referer )
        myquery.save()
        # messages.info(request, "New Candidate Added.")
        return redirect('adminportal')
        
    return render(request, "adminportal.html")


def delete(request, id):
    ref = Students.objects.filter(id=id)
    ref.delete()
    
    context = {
        'ref':ref,
    }
    return redirect("adminportal")


# Dashboard Functions

def dashboard(request):
    ref = Students.objects.filter(referer=request.user)
    total_rows = Students.objects.filter(referer=request.user).count()
    total_joined = Students.objects.filter(referer=request.user, status="Admission").count()

    # Define the course commission mapping
    course_commission = {
        "Business Analytics": 300,
        "Data Analytics": 500,
        "Data Science": 800,
        "Machine Learning": 1000,
        "Artificial Intelligence": 2000,
        "Web Development": 500,
        "Other": 300,
    }

    # Calculate the total commission for courses where status is "Admission Confirmed"
    total_commission = 0
    for entry in ref:
        if entry.status == "Admission" and entry.course in course_commission:
            total_commission += course_commission[entry.course]

    context = {
        "ref": ref,
        "total_rows": total_rows,
        "total_joined": total_joined,
        "total_commission": total_commission,
    }

    return render(request, "dashboard.html", context)




def add_dash(request): 
    if request.method == "POST":
        name = request.POST.get("name")
        pnumber = request.POST.get("pnumber")

        # Check if phone number already exists
        if Students.objects.filter(phonenumber=pnumber).exists():
            messages.warning(request, "Phone Number is already registered!")
            return render(request, "dashboard.html")

        pnumber2 = request.POST.get("pnumber2")
        course = request.POST.get("course")
        email = request.POST.get("email")
        remarks = request.POST.get("remarks")
        referer = request.POST.get("referer")
        status = request.POST.get("status")

        # Save the new student record
        Students.objects.create(
            name=name, 
            phonenumber=pnumber, 
            alternatenumber=pnumber2, 
            course=course, 
            email=email, 
            remarks=remarks, 
            status=status, 
            referer=referer
        )

        messages.success(request, "New candidate added successfully!")
        return redirect("dashboard")
    
    return render(request, "dashboard.html")



# def add_dash(request): 
#     if request.method == "POST":
#         name=request.POST.get("name")
#         pnumber=request.POST.get("pnumber")

#         if Students.objects.filter(phonenumber=pnumber).exists():
#             messages.warning(request, "Phone Number is already registered!")
#             #return HttpResponse("password incorrect")
#             return render(request,'dashboard.html')
#         else:
#             pass

#         pnumber2=request.POST.get("pnumber2")
#         course=request.POST.get("course")
#         email=request.POST.get("email")
#         remarks=request.POST.get("remarks")
#         referer=request.POST.get("referer")
#         status=request.POST.get("status")

#         myquery=Students(name=name, phonenumber=pnumber, alternatenumber=pnumber2, course=course, email=email, remarks=remarks, status=status, referer=referer )
#         myquery.save()
#         #messages.info(request, "New Candidate Added.")
#         return redirect('dashboard')
    
#     return render(request, "dashboard.html")


def edit_dash(request):
    ref = Students.objects.all()

    context = {
        "ref":ref,
               }
    return render(request, "dashboard.html", context)




def update_dash(request, id):
    if request.method == "POST":
        name=request.POST.get("name")
        pnumber=request.POST.get("pnumber")
        pnumber2=request.POST.get("pnumber2")
        course=request.POST.get("course")
        email=request.POST.get("email")
        remarks=request.POST.get("remarks")
        referer=request.POST.get("referer")
        status=request.POST.get("status")
        

        myquery=Students(id=id, name=name, phonenumber=pnumber, alternatenumber=pnumber2, course=course, email=email, status=status, remarks=remarks, referer=referer )
        myquery.save()
        # messages.info(request, "New Candidate Added.")
        return redirect('dashboard')
        
    return render(request, "dashboard.html")






# Withdraw_admin Portal

def withdraw_admin(request):
    bank = Withdraw.objects.all()

    context = {
        "bank":bank,
               }
    return render(request, "withdraw_admin.html", context)

# def withdraw_add(request):
#     if request.method == "POST":
#         account_holder_name=request.POST.get("account_holder_name")
#         account_number=request.POST.get("account_number")
#         phonenumber=request.POST.get("phonenumber")
#         bankname=request.POST.get("bankname")
#         branch=request.POST.get("branch")
#         ifsc_code=request.POST.get("ifsc_code")
#         pannumber=request.POST.get("pannumber")
#         cancelled_cheque=request.FILES.get("cancelled_cheque")

#         remarks=request.POST.get("remarks")
#         status=request.POST.get("status")
#         referer=request.POST.get("referer")


#         myquery=Withdraw(account_holder_name=account_holder_name, account_number=account_number, phonenumber=phonenumber, 
#                          bankname=bankname, branch=branch, ifsc_code=ifsc_code, pannumber=pannumber, cancelled_cheque=cancelled_cheque,
#                            remarks=remarks, status=status, referer=referer )
#         myquery.save()
#         #messages.info(request, "New Candidate Added.")
#         return redirect('withdraw')
    
#     return render(request, "withdraw.html")




# Allowed file extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

def withdraw_add(request):
    if request.method == "POST":
        account_holder_name = request.POST.get("account_holder_name")
        account_number = request.POST.get("account_number")
        phonenumber = request.POST.get("phonenumber")
        bankname = request.POST.get("bankname")
        branch = request.POST.get("branch")
        ifsc_code = request.POST.get("ifsc_code")
        pannumber = request.POST.get("pannumber")
        remarks = request.POST.get("remarks")
        status = request.POST.get("status")
        referer = request.POST.get("referer")

        # ✅ Handle file upload safely
        cancelled_cheque = request.FILES.get("cancelled_cheque")

        # ✅ Check if a file was uploaded
        cancelled_cheque = request.FILES.get("cancelled_cheque")
        if cancelled_cheque:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'cancelled_cheques'))
            filename = fs.save(cancelled_cheque.name, cancelled_cheque)
            cheque_url = 'cancelled_cheques/' + filename  # This stores relative path in DB
            print(f"File uploaded to: {cheque_url}")  # Debugging output
        else:
            cheque_url = None

        # ✅ Save data
        myquery = Withdraw(
            account_holder_name=account_holder_name,
            account_number=account_number,
            phonenumber=phonenumber,
            bankname=bankname,
            branch=branch,
            ifsc_code=ifsc_code,
            pannumber=pannumber,
            cancelled_cheque=cheque_url,
            remarks=remarks,
            status=status,
            referer=referer
        )
        myquery.save()

        messages.success(request, "Bank details added successfully!")
        return redirect("withdraw_admin")
    
    return render(request, "withdraw_admin.html")

def withdraw_edit(request):
    ref = Withdraw.objects.all()

    context = {
        "ref":ref,
               }
    return render(request, "withdraw_admin.html", context)

def withdraw_update(request, id):
    if request.method == "POST":
        name=request.POST.get("name")
        pnumber=request.POST.get("pnumber")
        pnumber2=request.POST.get("pnumber2")
        course=request.POST.get("course")
        email=request.POST.get("email")
        remarks=request.POST.get("remarks")
        referer=request.POST.get("referer")
        status=request.POST.get("status")
        

        myquery=Students(id=id, name=name, phonenumber=pnumber, alternatenumber=pnumber2, course=course, email=email, status=status, remarks=remarks, referer=referer )
        myquery.save()
        # messages.info(request, "New Candidate Added.")
        return redirect('withdraw_admin')
        
    return render(request, "withdraw_admin.html")


def withdraw_delete(request, id):
    ref = Students.objects.filter(id=id)
    ref.delete()
    
    context = {
        'ref':ref,
    }
    return redirect("withdraw_admin")






# Withdraw Dash Functions

def dash_withdraw(request):
    ref = Students.objects.filter(referer=request.user)
    total_rows = Students.objects.filter(referer=request.user).count()
    total_joined = Students.objects.filter(referer=request.user, status="Admission").count()

    # Define the course commission mapping
    course_commission = {
        "Business Analytics": 300,
        "Data Analytics": 500,
        "Data Science": 800,
        "Machine Learning": 1000,
        "Artificial Intelligence": 2000,
        "Web Development": 500,
        "Other": 300,
    }

    # Calculate the total commission for courses where status is "Admission Confirmed"
    total_commission = 0
    for entry in ref:
        if entry.status == "Admission" and entry.course in course_commission:
            total_commission += course_commission[entry.course]

    context = {
        "ref": ref,
        "total_rows": total_rows,
        "total_joined": total_joined,
        "total_commission": total_commission,
    }

    return render(request, "withdraw_dash.html", context)



def add_withdraw(request): 
    if request.method == "POST":
        name=request.POST.get("name")
        pnumber=request.POST.get("pnumber")
        pnumber2=request.POST.get("pnumber2")
        course=request.POST.get("course")
        email=request.POST.get("email")
        remarks=request.POST.get("remarks")
        referer=request.POST.get("referer")
        status=request.POST.get("status")

        myquery=Students(name=name, phonenumber=pnumber, alternatenumber=pnumber2, course=course, email=email, remarks=remarks, status=status, referer=referer )
        myquery.save()
        #messages.info(request, "New Candidate Added.")
        return redirect('dashboard')
    
    return render(request, "withdraw_dash.html")


def edit_withdraw(request):
    ref = Students.objects.all()

    context = {
        "ref":ref,
               }
    return render(request, "withdraw_dash.html", context)




def update_withdraw(request, id):
    if request.method == "POST":
        name=request.POST.get("name")
        pnumber=request.POST.get("pnumber")
        pnumber2=request.POST.get("pnumber2")
        course=request.POST.get("course")
        email=request.POST.get("email")
        remarks=request.POST.get("remarks")
        referer=request.POST.get("referer")
        status=request.POST.get("status")
        

        myquery=Students(id=id, name=name, phonenumber=pnumber, alternatenumber=pnumber2, course=course, email=email, status=status, remarks=remarks, referer=referer )
        myquery.save()
        # messages.info(request, "New Candidate Added.")
        return redirect('withdraw_dash')
        
    return render(request, "withdraw_dash.html")


