import frappe
from frappe import _

def get_context(context):
    # Get the color from the query parameter, default to black if not provided
    color = frappe.form_dict.color or 'black'
    context.color = color