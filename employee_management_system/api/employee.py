import frappe 
from frappe import _


@frappe.whitelist(allow_guest=False, methods=["GET" , "POST" , "PATCH" , "DELETE"])
def employee(**kwargs):
	"""
    Main function to handle employee-related operations.
    
    Args:
        kwargs: Dictionary of key-value pairs sent via request (e.g., for filtering, creating, updating, or deleting employees).
    
    Functionality:
        - Routes the request to the appropriate CRUD operation based on the HTTP method.
    
    Returns:
        JSON response with an HTTP status code and a message indicating the outcome.
    """
	try:
		if frappe.request.method == 'GET':
			get_employees(kwargs)
			
		if frappe.request.method == 'POST':
			create_employee(kwargs)
			
		if frappe.request.method == 'PATCH':
			edit_employee(kwargs)
			
		if frappe.request.method == 'DELETE':
			delete_employee(kwargs)
			

	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in employee'))
		frappe.local.response['message'] = _(e)


def edit_employee(kwargs):
	"""
    Updates the specified fields in an employee record.

    Args:
        kwargs: Key-value pairs to update an employee. Required:
            - employee: Employee ID to update.
            - Additional key-value pairs corresponding to fields to update (e.g., department, mobile_number).

    Returns:
        JSON response with an HTTP status code and a message indicating successful update.
    """
	try:
		employee = kwargs.get("employee")
		if not employee:
			frappe.local.response['http_status_code'] = 400
			frappe.log_error(message=str(e), title=_('Error in edit_employee'))
			frappe.local.response['message'] = str(e)
			return

		kwargs.pop("employee", None)

		for field, value in kwargs.items():
			frappe.db.set_value("Employee", employee, field, value)

		frappe.local.response['http_status_code'] = 200
		frappe.local.response['message'] = _(f"Employee {employee} updated successfully")
		
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in edit_employee'))
		frappe.local.response['message'] = str(e)

def delete_employee(kwargs):
	"""
    Deletes an employee record.

    Args:
        kwargs: Required key:
            - employee: Employee ID to delete.

    Returns:
        JSON response with an HTTP status code and a message indicating successful deletion.
    """
	try:
		employee = kwargs.get("employee")
		if not employee:
			frappe.local.response['http_status_code'] = 400
			frappe.log_error(message=str(e), title=_('Error in delete_employee'))
			frappe.local.response['message'] = str(e)
			return
		
		doc = frappe.get_doc("Employee",employee)
		doc.delete()
		frappe.db.commit()
		frappe.local.response['http_status_code'] = 200
		frappe.local.response['message'] = _(f"""The Employee deleted""")
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in delete_employee'))
		frappe.local.response['message'] = _(e)

def create_employee(kwargs):
	"""
    Creates a new employee record.

    Args:
        kwargs: Key-value pairs to create a new employee. Required fields:
            - employee_name: Name of the employee.
            - company: Company the employee belongs to.
            - department: Employee's department.
            - email_address: Employee's email address.
            - mobile_number: Employee's mobile number.
            - hired_on: Hiring date.

    Returns:
        JSON response with an HTTP status code and a message indicating successful creation.
    """
	try:
		doc = frappe.new_doc("Employee")
		doc.employee_name = kwargs.employee_name
		doc.company = kwargs.company
		doc.department = kwargs.department
		doc.email_address = kwargs.email_address
		doc.mobile_number = kwargs.mobile_number
		doc.hired_on = kwargs.hired_on
		doc.save()
		frappe.db.commit()
		
		frappe.local.response['http_status_code'] = 200
		frappe.local.response['message'] = _(f"""New Employee created""")
		
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in create_employee'))
		frappe.local.response['message'] = _(e)


def get_employees(kwargs):
	"""
    Fetches a list of employees with specified fields.

    Args:
        kwargs: Optional filters for retrieving employees (e.g., by status, company, etc.).

    Returns:
        JSON response with an HTTP status code and the list of employee details under the `employees` key.
    """
	try:
		res = frappe.get_list("Employee",
						[
							'employee_name',
							'status',
							'company'
							'department',
							'email_address',
							'mobile_number',
							'hired_on',
							'days_employed',
							'number_of_assigned_projects'
						])
		frappe.local.response['http_status_code'] = 200
		frappe.local.response['employees'] = res
		
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in get_employees'))
		frappe.local.response['message'] = _(e)
