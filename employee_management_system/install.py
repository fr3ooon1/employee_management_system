import frappe

def after_install():
	print("Create Workflow Statues")
	create_status()
	
    
def create_status():
	status = [
		{
			"workflow_state_name":"Not Accepted",
		},
		{
			"workflow_state_name":"Hired",
		},
		{
			"workflow_state_name":"Interview Scheduled",
		},
		{
			"workflow_state_name":"Application Received",
		},
		
	]
	for i in status:
		if not frappe.db.exists("Workflow State",i.get("workflow_state_name")):
			status = frappe.new_doc("Workflow State")
			status.workflow_state_name = i.get("workflow_state_name")
			status.insert(ignore_permissions=True)