from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Employee
from django.shortcuts import render
from django.utils import timezone

@shared_task
def send_expiration_reminders():
    two_months_from_now = timezone.now() + timedelta(days=60)
    employees = Employee.objects.filter(
        passport_expiry_date__lte=two_months_from_now,
        passport_expiry_date__gte=timezone.now()
    ) | Employee.objects.filter(
        brp_expiry_date__lte=two_months_from_now,
        brp_expiry_date__gte=timezone.now()
    )
    for employee in employees:
        send_mail(
            'Reminder: Document Expiration',
            f'Dear {employee.first_name},\n\n'
            'This is a reminder that your document(s) will expire soon.\n'
            'Passport Expiry Date: {employee.passport_expiry_date}\n'
            'BRP Expiry Date: {employee.brp_expiry_date}\n\n'
            'Please take the necessary actions.\n\n'
            'Best regards,\nHR Team',
            'your_hr_email@gmail.com',
            [employee.email],
            fail_silently=False,
        )


