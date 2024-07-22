# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	message = ''
	return get_columns(filters), make_data(filters), message, get_chart(), get_report_summary()

def get_columns(filters=None):
    return [
        {
            "fieldname": 'airline',
            "label": 'Airline',
            "fieldtype": 'Link',
            "options": 'Airline',
            "width": '150px',
        },
        {
            "fieldname": 'revenue',
            "label": 'Revenue',
            "fieldtype": 'Currency',
            "width": '150px',
        },
    ]

def make_data(filters=None):
    data = []
    airlines = frappe.get_all("Airline", pluck="name")
    
    airline_revenue = frappe.db.sql(
        """
            SELECT SUM(ticket.total_amount) as revenue, airplane.airline as airline 
            FROM `tabAirplane Flight` flight 
            INNER JOIN `tabAirplane Ticket` ticket ON ticket.flight = flight.name
            LEFT JOIN `tabAirplane` airplane ON airplane.name = flight.airplane
            WHERE airplane.airline IN (%s)
            GROUP BY airplane.airline
        """ % ','.join(['%s'] * len(airlines)),
        tuple(airlines),
        as_dict=True
    )

    airline_revenue_dict = {item['airline']: item['revenue'] for item in airline_revenue}

    for airline in airlines:
        data.append({
            "airline": airline,
            "revenue": airline_revenue_dict.get(airline, 0.00)
        })

    return data

def get_chart():
	data = make_data(filters=None)
	labels = [item['airline'] for item in data]
	datasets = [
		{"name": "Revenue", "values": [item['revenue'] for item in data]}
	]
	chart = {"data": {"labels": labels, "datasets": datasets}, "type": "donut"}

	return chart

def get_report_summary():
	data = make_data(filters=None)
	total = sum(row.get("revenue", 0) for row in data)
	report_summary = [
		{"value": total, "label": "Total Revenue", "datatype": "Currency"}
	]
	return report_summary
