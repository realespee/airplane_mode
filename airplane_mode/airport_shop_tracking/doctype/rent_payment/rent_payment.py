# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class RentPayment(Document):
	def before_save(self):
		self.total_payment = self.set_first_payment()
		self.payment_due_date = self.set_payment_due_date().date()
	def on_submit(self):
		self.confirm_receipt_number()
		self.submit_tenant_and_contract()
		self.change_shop_status()
		self.convert_application()

	def set_payment_due_date(self):
		freq = frappe.db.get_value('Tenant Contract', {'tenant': self.tenant}, 'payment_frequency')
		if freq and freq == 'Monthly':
			return datetime.today() + timedelta(days=30)
		if freq and freq == 'Annually':
			return datetime.today() + timedelta(days=365)

	def set_first_payment(self):
		tenants = []
		payment_frequency = frappe.db.get_single_value('Shop Tracking Settings', 'initial_payable_months')
		contracts = frappe.get_all('Tenant Contract', fields = ['tenant'], filters={'docstatus':1})
		for c in contracts:
			if c.tenant == self.tenant:
				tenants.append(c)
			
		if not len(tenants):
			return self.amount * int(payment_frequency)

	def confirm_receipt_number(self):
		if not self.receipt_number:
			frappe.throw(_('Receipt Number Missing!'))

	def submit_tenant_and_contract(self):
		tenant = frappe.get_doc('Tenant', self.tenant)
		tenant_contract = frappe.get_doc('Tenant Contract', self.tenant_contract)
		tenant.status = 'Active'
		tenant.save()
		tenant_contract.submit()

	def change_shop_status(self):
		shop = frappe.get_doc('Shop', self.shop)
		shop.status = 'Leased'
		shop.save()

	def convert_application(self):
		applicant = frappe.db.get_value('Tenant', self.tenant, 'shop_leasing_applicant')
		doc = frappe.get_doc('Shop Leasing Application', applicant)
		doc.status = 'Converted'
		doc.save()