import frappe
from frappe import _

@frappe.whitelist()
def get_sales_invoice_for_reservation(reservation_name):
    sales_invoice = frappe.get_all(
        "Sales Invoice",
        filters={"custom_reservation": reservation_name, "docstatus": 1},
        fields=["name"]
    )

    if sales_invoice:
        return sales_invoice[0].name 
    else:
        frappe.msgprint(_("No Sales Invoice found for this reservation."))
        return None
