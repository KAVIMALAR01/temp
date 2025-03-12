import frappe

def on_cancel(doc,method):
    #frappe.msgprint("cancelled")
    #frappe.msgprint(f"Employeee- {doc.owner}.")
    frappe.enqueue(send_rejection_email, queue='short', doc=doc)

def on_update_after_submit(doc, method):
    if doc.workflow_state == "Approved":
        frappe.db.set_value("Sales Order", doc.name, "is_approved", 1)
        frappe.enqueue(send_approval_email, queue='short', doc=doc)
     
def send_approval_email(doc):
    sales_manager_email = frappe.db.get_value("Employee", {"designation": "Sales Manager"}, ["user_id"])
    
    if sales_manager_email:
        subject = f"Sales Order {doc.name} Approved"
        message = f"""
            <div style="font-family: Arial, sans-serif; border: 1px solid #d1d1d1; padding: 15px; border-radius: 8px;">
                <h2 style="color: #28a745;">Sales Order Approved </h2>
                <p>Dear Sales Manager,</p>
                <p>The Sales Order <strong>{doc.name}</strong> has been <span style="color: #28a745;"><b>approved</b></span>.</p>
                <p>Please review it for final approval.</p>
                <hr>
                <p style="color: #555;">Best Regards,<br><strong>Info Company</strong></p>
            </div>
        """
        frappe.sendmail(recipients=sales_manager_email, subject=subject, message=message)
        frappe.msgprint(f"Approval email sent to Sales Manager ({sales_manager_email}).")

def send_rejection_email(doc , method):
    recipient_email = None
    if not doc.is_approved:  
        recipient_email = doc.owner
    else:
        recipient_email = frappe.db.get_value("Employee", {"designation": "Sales Supervisor"}, "user_id")

    if recipient_email:
        subject = f"Sales Order {doc.name} Rejected"
        message = f"""
            <div style="font-family: Arial, sans-serif; border: 1px solid #f8d7da; padding: 15px; border-radius: 8px; background-color: #f8d7da;">
                <h2 style="color: #dc3545;">Sales Order Rejected </h2>
                <p>Hello,</p>
                <p>The Sales Order <strong>{doc.name}</strong> has been <span style="color: #dc3545;"><b>rejected</b></span></p>
                <p>Kindly take necessary action.</p>
                <hr>
                <p style="color: #555;">Best Regards,<br><strong>Info Company</strong></p>
            </div>
        """
        frappe.sendmail(recipients=recipient_email, subject=subject, message=message)
        frappe.msgprint(f"Rejection email sent to {recipient_email}.")



'''@frappe.whitelist()
def get_sales_invoices(sales_order):
    invoices = frappe.get_all(
        "Sales Invoice",
        filters={"sales_order": sales_order},
        pluck="name"
    )
    return invoices '''
