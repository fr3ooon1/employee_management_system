import frappe 
from frappe import _


@frappe.whitelist(allow_guest=False, methods=["GET"])
def get_employees(**kwargs):
	try:
		if frappe.request.method == 'GET':
			get_departments(kwargs)
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in get_employees'))
		frappe.local.response['message'] = _(e)


def get_departments(kwargs):
	try:
		res = frappe.get_list("Department",
						[
							'company',
							'name_of_department',
							'number_of_employees',
							'number_of_projects'
						])
		frappe.local.response['http_status_code'] = 200
		frappe.local.response['departments'] = res
		
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in get_departments'))
		frappe.local.response['message'] = _(e)
