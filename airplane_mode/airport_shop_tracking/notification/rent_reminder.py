
import frappe
from frappe.utils import get_url, nowdate
import random


@frappe.whitelist()
def send_reminder():
    due_payments = get_rent_payments_due_in_5_days()
    rent_reminder_setting = frappe.db.get_single_value('Shop Tracking Settings', 'enable_rent_reminders')
    if len(due_payments) and rent_reminder_setting == 1:
        recipients = [t['tenant_email'] for t in due_payments]
        for payment in due_payments:
            frappe.sendmail(
                recipients=recipients,
                subject=frappe._(f'Rent For Shop {payment["shop"]} is Due in Five Days'),
                header=_('Rent Due in Five Days'),
                message=email_message(payment['tenant'], payment['amount'], payment['payment_due_date'], payment['shop'])
            )

def email_message(name, amount_due, due_date, shop):
    return f'''
        <div class="container" style="max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <div class="text-center bg-success text-white py-2">
                <h1 class="h3">Rent Due Reminder</h1>
            </div>
            <div class="mt-4">
                <p>Dear {name},</p>
                <p>This is a friendly reminder that your rent for Shop {shop} of <strong>{amount_due}</strong> is due on <strong>{due_date}</strong>.</p>
                <p>Please ensure that your payment is made by the due date to avoid any late fees.</p>
                <p>If you have any questions or concerns, feel free to contact us.</p>
                <a href="#" class="btn btn-success btn-block mt-3">Pay Now</a>
            </div>
            <div class="text-center mt-4">
                <p>Thank you for your prompt attention to this matter.</p>
                <p>Best regards,</p>
                <p>Airport Services</p>
            </div>
        </div>
    '''

def get_rent_payments_due_in_5_days():
    # Calculate the date 5 days from today
    target_date = datetime.today() + timedelta(days=5)
    target_date_str = target_date.strftime('%Y-%m-%d')

    # Use frappe.get_list to get records where payment_due_date is 5 days away
    rent_payments = frappe.get_list(
        'Rent Payment',
        filters={'payment_due_date': target_date_str},
        fields=['shop', 'tenant', 'payment_due_date', 'amount']
    )

    # Collect tenant emails
    for payment in rent_payments:
        tenant_email = frappe.get_value('Tenant', payment.tenant, 'email')
        payment['tenant_email'] = tenant_email

    return rent_payments