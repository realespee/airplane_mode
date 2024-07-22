# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ShopLeasingApplication(Document):
	def on_submit(self):
		self.create_new_tenant_contract()
		
	def create_new_tenant_contract(self):
		# create tenant
		self.create_new_tenant()
		# if tenant, create contract
		tenant = frappe.db.get_value('Tenant', {'shop_leasing_applicant': self.name}, 'name')
		if(tenant and self.status == 'Approved'):
			
			frappe.get_doc(
				{
					"doctype": "Tenant Contract",
					"tenant": tenant,
					"shop": self.shop,
					"monthly_remittance": self.price,
					"address": self.address,
					"amount": self.price * 12
				}
			).insert(ignore_permissions=True)

			frappe.db.commit()

		if(self.status == 'Approved'):
			self.change_shop_status('Booked')
	def create_new_tenant(self):
		if(self.status == 'Approved'):
			frappe.get_doc(
				{
					"doctype": "Tenant",
					"tenant_name": self.first_name + " " + self.last_name,
					"email": self.email_id,
					"phone": self.phone,
					"address": self.address,
					"shop_leasing_applicant": self.name
				}
			).insert(ignore_permissions=True)

			frappe.db.commit()

	def change_shop_status(self, status):
		shop = frappe.get_doc('Shop', self.shop)
		shop.status = status
		shop.save()