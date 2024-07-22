# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import random
import string


class AirplaneTicket(Document):
	def before_save(self):
		self.total_amount = self.calculate_total_amount()

	def validate(self):
		self.remove_duplicate_addons()
		self.validate_seat_capacity()

	def before_insert(self):
		self.seat = self.create_seat_number()

	def before_submit(self):
		self.confirm_boarded_on_submit()

	def calculate_total_amount(self):
		adons_amounts = [addon.amount for addon in self.add_ons]
		return sum(adons_amounts) + int(self.flight_price)

	def remove_duplicate_addons(self):
		if self.get('add_ons'):
			unique_add_ons = []
			duplicate_indices = []
			seen = set()

			for idx, add_on in enumerate(self.add_ons):
				identifier = (add_on.item)
				if identifier in seen:
					duplicate_indices.append(idx)
				else:
					seen.add(identifier)
					unique_add_ons.append(add_on)

			for idx in reversed(duplicate_indices):
				self.add_ons.remove(self.add_ons[idx])

	def confirm_boarded_on_submit(self):
		if not self.status == "Boarded":
			frappe.throw("Airplane ticket must be in 'Boarded' status before Submit")

	def create_seat_number(self):
		random_integer = random.randint(10, 99)
		random_alphabet = random.choice('ABCDE')
		return f"{random_integer}{random_alphabet}"

	def validate_seat_capacity(self):
		flight = frappe.get_doc('Airplane Flight', self.flight)
		airplane = frappe.get_doc('Airplane',flight.airplane)
		ticket_count = frappe.db.count('Airplane Ticket', {'flight': self.flight})
		if ticket_count >= airplane.capacity:
			frappe.throw(f"The number of tickets for this flight exceeds the airplane's capacity of {airplane.capacity} seats.")

