# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator, Document):
	def on_submit(self):
		self.confirm_gate_number()
		self.update_flight_status()
	def on_update(self):
		self.update_ticket_gate_numbers()
		self.notify_passengers_on_flight_changes()
	def confirm_gate_number(self):
		if not self.gate_number:
			frappe.throw('Please Assign <strong>Gate Number</strong> to this Flight!')

	def update_flight_status(self):
		if not self.status == 'Completed':
			self.status = 'Completed'
	def update_ticket_gate_numbers(self):
		flight_tickets = frappe.get_all('Airplane Ticket', {'flight': self.name}, pluck='name')
		if len(flight_tickets):
			for ticket in flight_tickets:
				doc = frappe.get_doc('Airplane Ticket', ticket)
				doc.gate_number = self.confirm_gate_number
				doc.save()

	def notify_passengers_on_flight_changes(self):
		# Send Notification for Gate Changes
		passenger_emails = []
		flight_passengers = frappe.get_all('Airplane Ticket', {'flight': self.name}, pluck='passenger')
		if len(flight_passengers):
			for passenger in flight_passengers:
				email = frappe.get_value('Flight Passenger', passenger, 'email_id')
				passenger_emails.append(email)
			
		frappe.sendmail(
                recipients=passenger_emails,
                subject=frappe._(f'Change of Gate Number for Flight {self.name}'),
                header=_('Change in Flight Gate Number'),
                message=self.notification_message()
            )	
	def notification_message(self):
		return f'''
			<div class="container" style="max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
				<div class="text-center bg-success text-white py-2">
					<h1 class="h3">Change in Gate Number for Flight {self.name}</h1>
				</div>
				<div class="mt-4">
					<p>Dear Passenger,</p>
					<p>There has been a Change in Boarding Gate for Flight {self.name} to {self.gate_number}</strong>.</p>
					<p>We apologize for any incoveniences!</p>
					<p>If you have any questions or concerns, feel free to contact us.</p>
					<a href="#" class="btn btn-success btn-block mt-3">Pay Now</a>
				</div>
				<div class="text-center mt-4">
					<p>Thank you for your prompt attention to this matter.</p>
					<p>Best regards,</p>
					<p>{self.source_airport}</p>
				</div>
        	</div>
		'''