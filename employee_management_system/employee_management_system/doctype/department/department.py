# Copyright (c) 2024, Muhammad Essam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Department(Document):
	def on_update(self):
		self.count_department()

	def on_trash(self):
		frappe.throw(_("Cannot delete this document"))

	def count_department(self):
		if self.company:
			counter = frappe.db.count("Department", filters={"company": self.company})
			doc_company = frappe.get_doc("Company" , self.company)
			doc_company.number_of_departments = counter
			doc_company.save(ignore_permissions=True)
		
		frappe.db.commit()
