from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
import fitz  # PyMuPDF
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Employee


def notify():
    alert_threshold_date = timezone.now().date() + timedelta(days=60)
    current_date = timezone.now().date()

    # Query employees with upcoming passport or BRP expirations
    upcoming_passport_expirations = Employee.objects.filter(
        passport_expiry_date__lte=alert_threshold_date,
        passport_expiry_date__gte=current_date
    )
    upcoming_brp_expirations = Employee.objects.filter(
        brp_expiry_date__lte=alert_threshold_date,
        brp_expiry_date__gte=current_date
    )

    # Create alerts with the required fields
    alerts = [
                 {
                     'employee': employee,
                     'type': 'passport',
                     'date': employee.passport_expiry_date
                 }
                 for employee in upcoming_passport_expirations
             ] + [
                 {
                     'employee': employee,
                     'type': 'brp',
                     'date': employee.brp_expiry_date
                 }
                 for employee in upcoming_brp_expirations
             ]

    context = {
        'alerts': alerts,
        'alerts_count': len(alerts),
    }
    return context


def loginn(request):
    return render(request, 'login.html')


def signin(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("/add_employee/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=name, password=password)

            if user is not None:
                login(request, user)
                return redirect("/add_employee/")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect('/signin/')
        return render(request, "login.html")


def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("/")


def add_employee(request):
    notifications = notify()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        email = request.POST['email']
        position = request.POST['position']
        phone_number = request.POST['phone_number']
        passport_expiry_date = request.POST['passport_expiry_date']
        brp_expiry_date = request.POST['brp_expiry_date']
        passport_document = request.FILES['passport_document']
        brp_document = request.FILES['brp_document']

        employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=email,
            position=position,
            phone_number=phone_number,
            passport_expiry_date=passport_expiry_date,
            brp_expiry_date=brp_expiry_date,
            passport_document=passport_document,
            brp_document=brp_document
        )
        print(f"Employee ID: {employee.id}")

        return redirect('generate_filled_pdf', employee_id=employee.id)
    context = {
        'alerts': notifications['alerts'],
    }
    return render(request, 'index.html', context)


def generate_filled_pdf(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        current_date = timezone.now().strftime('%B %d, %Y')  # Format as 'Month Day, Year'
        pdf_path = '/Users/anshuanto/Downloads/Hr checklist app/HRchecklist/templates/Offerletter.pdf'
        output_path = os.path.join('static', f'offer_letter_{employee_id}.pdf')
        pdf_document = fitz.open(pdf_path)
        page = pdf_document[0]

        # Fill in the details with specific coordinates
        page.insert_text((115, 280), employee.first_name, fontsize=10)
        page.insert_text((265, 339), employee.position, fontsize=10)
        page.insert_text((265, 387), employee.salary, fontsize=10)
        page.insert_text((115, 220), current_date, fontsize=10)
        page.insert_text((293, 597), 'HR@company.com', fontsize=10)

        pdf_document.save(output_path)
        pdf_document.close()

        with open(output_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="offer_letter_{employee_id}.pdf"'
            return response
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found.")


def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': Employee.objects.filter(email=email).exists()
    }
    return JsonResponse(data)


def send_email_view(request):
    notifications = notify()

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject and message:
            # Get all employee emails
            emails = Employee.objects.values_list('email', flat=True)

            # Send email to each address
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                emails,
                fail_silently=False,
            )

            messages.success(request, f'An email with the subject "{subject}" has been sent to all employees.')
            return redirect('send_email')  # Redirect to the same page to show the message
        else:
            messages.error(request, 'Both subject and message are required.')
    context = {
        'alerts': notifications['alerts'],
    }
    return render(request, 'send_email.html', context)


def employee_list(request):
    notifications = notify()
    employees = Employee.objects.all()

    context = {
        'alerts': notifications['alerts'],
        'employees': employees,
    }

    return render(request, 'employee_details.html', context)


def update_employee(request):
    if request.method == 'POST':
        # Process the form and update the employee
        employee_id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        position = request.POST.get('position')
        phone_number = request.POST.get('phone_number')

        # Fetch the employee object and update it
        try:
            employee = Employee.objects.get(id=employee_id)
            employee.first_name = first_name
            employee.last_name = last_name
            employee.email = email
            employee.position = position
            employee.phone_number = phone_number
            employee.save()
            return JsonResponse({'status': 'success'})
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Employee not found'})
    else:
        # Return an error or redirect if the method is not POST
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def delete_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('id')
        employee = get_object_or_404(Employee, id=employee_id)
        employee.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
