# Copyright (c) 2024, Muhammad Essam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import re
from frappe.model.document import Document

class Employee(Document):
	def validate(self):
		self.validate_email()
		self.calculate_days_employed()
		self.validate_mobile_number()
	
	def on_trash(self):
		frappe.throw(_("Cannot delete this document"))

	def on_update(self):
		self.count_department_and_companies()

	def validate_email(self):
		if (not self.email_address) or  (not re.match(r"[^@]+@[^@]+\.[^@]+", self.email_address)):
			frappe.throw(_("Invalid Email Address"))
	
	def count_department_and_companies(self):
		if self.department:
			counter = frappe.db.count("Employee", filters={"department": self.department})
			doc = frappe.get_doc("Department" , self.department)
			doc.number_of_employees = counter
			doc.save(ignore_permissions=True)
		
		if self.company:
			counter = frappe.db.count("Employee", filters={"company": self.company})
			doc_company = frappe.get_doc("Company" , self.company)
			doc_company.number_of_employees = counter
			doc_company.save(ignore_permissions=True)

		frappe.db.commit()

	def calculate_days_employed(self):
		
		if self.hired_on:
			today = frappe.utils.today()
			hired_on = self.hired_on
			date_diff = frappe.utils.date_diff(today, hired_on)
			print(date_diff)
			self.days_employed = f"""{date_diff} days"""

	def validate_mobile_number(self):
		if self.mobile_number:
			pattern = r'^\+?[\d\s\-()]{11}$'
			va = bool(re.match(pattern, self.mobile_number))
			if not va :
				frappe.throw(_("Invalid Phone Number")) 
