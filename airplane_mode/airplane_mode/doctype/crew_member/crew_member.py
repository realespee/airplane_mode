# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CrewMember(Document):
	def before_save(self):
		self.full_name = f"{self.first_name} {self.last_name}" if self.last_name else self.first_name
