// Copyright (c) 2025, Kavi and contributors
// For license information, please see license.txt

frappe.query_reports["Reservation Reports"] = {
    "filters": [
        {
            "fieldname": "status",
            "label": "Reservation Status",
            "fieldtype": "Select",
            "options": "\nPending\nConfirmed\nChecked-in\nChecked-out\nCancelled",
            "default": "Confirmed"
        },
        {
            "fieldname": "guest",
            "label": "Guest",
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.nowdate(), -30)
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "default": frappe.datetime.nowdate()
        },
        {
            "fieldname": "room",
            "label": "Room",
            "fieldtype": "Link",
            "options": "Item"
        }
    ]
};
