# Copyright (c) 2024, Muhammad Essam and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Company(Document):
	def on_trash(self):
		frappe.throw(_("Cannot delete this document"))
