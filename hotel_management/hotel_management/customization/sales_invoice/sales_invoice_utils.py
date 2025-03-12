import frappe
from frappe.utils import now_datetime, get_datetime

def _get_time_text(minutes):
    if minutes < 60:
        return f"{int(minutes)} minutes ago"
    elif minutes < 1440:
        return f"{int(minutes // 60)} hours ago"
    return f"{int(minutes // 1440)} days ago"
def test_sales_invoice_event():
    try:
        cron_settings = frappe.get_single("CRON")
        last_updated = cron_settings.last_updated
        if last_updated:
            last_updated = get_datetime(last_updated)
        else:
            last_updated = now_datetime()  
        frequency = cron_settings.frequency or 10  
        current_time = now_datetime()
        time_since_last_update = (current_time - last_updated).total_seconds() / 60
        if time_since_last_update < frequency:
            return 
        frappe.log_error("✅ Sales Invoice Scheduled Event is Running!", "Scheduled Task Log")
        sales_invoices = frappe.get_all(
            "Sales Invoice",
            filters={"docstatus": 1}, 
            fields=["name", "creation", "custom_invoice_duration"]
        )
        for invoice in sales_invoices:
            time_since_creation = (current_time - invoice["creation"]).total_seconds() / 60  
            if time_since_creation >= frequency:
                frappe.db.set_value("Sales Invoice", invoice["name"], "custom_invoice_duration", _get_time_text(time_since_creation))
        frappe.db.set_value("CRON", None, "last_updated", current_time.strftime("%Y-%m-%d %H:%M:%S"))
        frappe.db.commit()
        frappe.log_error("✅ Sales Invoice durations updated successfully!", "Scheduled Task Log")   
    except Exception as e:
        frappe.log_error(f"❌ Error: {str(e)}", "Scheduled Task Error")
