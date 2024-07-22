# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


from datetime import datetime, timedelta


class TenantContract(Document):
	def before_save(self):
		self.payment_due_date = self.set_payment_due_date().date()
		self.contract_date_of_expiry = (datetime.today() + timedelta(days=365)).date()
	def set_payment_due_date(self):
		freq = self.payment_frequency
		if freq and freq == 'Monthly':
			return datetime.today() + timedelta(days=30)
		if freq and freq == 'Annually':
			return datetime.today() + timedelta(days=365)