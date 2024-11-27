import frappe 
from frappe import _


@frappe.whitelist(allow_guest=False, methods=["GET" , "POST" , "PATCH" , "DELETE"])
def project(**kwargs):

	try:
		if frappe.request.method == 'GET':
			get_projects(kwargs)
			
		if frappe.request.method == 'POST':
			create_project(kwargs)
			
		if frappe.request.method == 'PATCH':
			edit_project(kwargs)
			
		if frappe.request.method == 'DELETE':
			delete_project(kwargs)
			

	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in project'))
		frappe.local.response['message'] = _(e)


def edit_project(kwargs):
	try:
		project = kwargs.get("project")
		if not project:
			frappe.local.response['http_status_code'] = 400
			frappe.log_error(message=str(e), title=_('Error in edit_project'))
			frappe.local.response['message'] = str(e)
			return
		
		doc = frappe.get_doc("Project",project)
		doc.project_name = kwargs.get("project_name") if kwargs.get("project_name") else doc.project_name 
		doc.project_name = kwargs.get("company") if kwargs.get("company") else doc.company 
		doc.project_name = kwargs.get("department") if kwargs.get("department") else doc.department 
		doc.project_name = kwargs.get("description") if kwargs.get("description") else doc.description 
		doc.project_name = kwargs.get("start_date") if kwargs.get("start_date") else doc.start_date 
		doc.project_name = kwargs.get("end_date") if kwargs.get("end_date") else doc.end_date 

		if kwargs.get("employee"):
			for employee in kwargs.get("employee"):
				doc.append("table_jcnh",{
					"employee":employee.name
				})
		doc.save()
		frappe.db.commit()

		frappe.local.response['http_status_code'] = 200
		frappe.local.response['message'] = _(f"project {project} updated successfully")
		
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in edit_employee'))
		frappe.local.response['message'] = str(e)

def delete_project(kwargs):
	try:
		project = kwargs.get("project")
		if not project:
			frappe.local.response['http_status_code'] = 400
			frappe.log_error(message=str(e), title=_('Error in delete_project'))
			frappe.local.response['message'] = str(e)
			return
		
		doc = frappe.get_doc("Project",project)
		doc.delete()
		frappe.db.commit()
		frappe.local.response['http_status_code'] = 200
		frappe.local.response['message'] = _(f"""The Project deleted""")
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in delete_project'))
		frappe.local.response['message'] = _(e)

def create_project(kwargs):
	try:
		doc = frappe.get_doc("Project",project)
		doc.project_name = kwargs.get("project_name") 
		doc.project_name = kwargs.get("company") 
		doc.project_name = kwargs.get("department") 
		doc.project_name = kwargs.get("description") 
		doc.project_name = kwargs.get("start_date") 
		doc.project_name = kwargs.get("end_date") 

		if kwargs.get("employee"):
			for employee in kwargs.get("employee"):
				doc.append("table_jcnh",{
					"employee":employee.name
				})

		doc.save()
		frappe.db.commit()
		
		frappe.local.response['http_status_code'] = 200
		frappe.local.response['message'] = _(f"""New Project created""")
		
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in create_project'))
		frappe.local.response['message'] = _(e)


def get_projects(kwargs):
	try:
		res = frappe.db.sql("""
					SELECT 
						project_name, 
						company, 
					  	(SELECT GROUP_CONCAT(employee) 
					  	FROM `tabAssigned Employees` 
					  	WHERE parent = tabProject.project_name) AS employees
					FROM `tabProject` ;
					""", as_dict=True)

		frappe.local.response['http_status_code'] = 200
		frappe.local.response['employees'] = res
		
	except Exception as e:
		frappe.local.response['http_status_code'] = 400
		frappe.log_error(message=str(e), title=_('Error in get_projects'))
		frappe.local.response['message'] = _(e)
