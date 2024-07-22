# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator


class Shop(WebsiteGenerator, Document):
	def before_save(self):
		default_rent_amount = frappe.db.get_single_value('Shop Tracking Settings', 'default_rent_amount')
		if default_rent_amount:
			if not self.price:
				self.price = default_rent_amount
