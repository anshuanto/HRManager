from celery import shared_task
from .models import Employee
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_expiration_reminders():
    two_months_from_now = timezone.now() + timedelta(days=1)
    employees = Employee.objects.filter(
        passport_expiry_date__lte=two_months_from_now,
        passport_expiry_date__gte=timezone.now()
    ) | Employee.objects.filter(
        brp_expiry_date__lte=two_months_from_now,
        brp_expiry_date__gte=timezone.now()
    )

    logger.info(f'Found {employees.count()} employees for reminders.')

    for employee in employees:
        logger.info(f'Sending email to {employee.email}.')
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


@shared_task
def send_email_to_even_numbered_employees():
    logger.info("Starting task: send_email_to_even_numbered_employees")

    employees = Employee.objects.filter(id__mod=2, id__gt=0)  # Employees with even IDs
    logger.info(f"Found {employees.count()} employees with even IDs")

    for employee in employees:
        logger.info(f"Sending email to {employee.email}")
        send_mail(
            'Reminder: HR Notification',
            f'Dear {employee.first_name},\n\n'
            'This is a periodic reminder.\n\n'
            'Best regards,\nHR Team',
            'your_hr_email@gmail.com',
            [employee.email],
            fail_silently=False,
        )
    logger.info("Task completed: send_email_to_even_numbered_employees")



