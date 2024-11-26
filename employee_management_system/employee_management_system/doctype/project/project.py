# Copyright (c) 2024, Muhammad Essam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Project(Document):
	def on_update(self):
		self.count_projects()
		self.get_all_employee_assign()

	def on_trash(self):
		frappe.throw(_("Cannot delete this document"))

	def count_projects(self):
		if self.department:
			counter = frappe.db.count("Project", filters={"department": self.department})
			doc_department = frappe.get_doc("Department" , self.department)
			doc_department.number_of_projects = counter
			doc_department.save(ignore_permissions=True)
			
		
		if self.company:
			counter = frappe.db.count("Project", filters={"company": self.company})
			doc_company = frappe.get_doc("Company" , self.company)
			doc_company.number_of_projects = counter
			doc_company.save(ignore_permissions=True)
		
		frappe.db.commit()

	def get_all_employee_assign(self):
		assingned_amployees = self.get("table_jcnh")

		for employee in assingned_amployees:
			temp = frappe.db.get_list("Assigned Employees",{
				"employee":employee.get("employee")
			})
			emp = frappe.get_doc("Employee",employee.get("employee"))
			emp.number_of_assigned_projects = len(temp)
			emp.save(ignore_permissions=True)
			frappe.db.commit()
