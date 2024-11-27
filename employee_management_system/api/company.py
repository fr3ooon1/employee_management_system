import frappe 
from frappe import _


@frappe.whitelist(allow_guest=False, methods=["GET"])
def company(**kwargs):
	try:
		if frappe.request.method == 'GET':
			get_companies(kwargs)
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in company'))
		frappe.local.response['message'] = _(e)


def get_companies(kwargs):
	try:
		res = frappe.get_list("Company",
						[
							'company_name',
							'number_of_departments',
							'number_of_employees',
							'number_of_projects'
						])
		frappe.local.response['http_status_code'] = 200
		frappe.local.response['companies'] = res
		
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in get_companies'))
		frappe.local.response['message'] = _(e)
