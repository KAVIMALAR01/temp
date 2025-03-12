# Copyright (c) 2025, Kavi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Reservation ID", "fieldname": "name", "fieldtype": "Link", "options": "Reservation", "width": 150},
        {"label": "Guest", "fieldname": "guest", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Room", "fieldname": "room", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Booking Date", "fieldname": "booking_date", "fieldtype": "Date", "width": 120},
        {"label": "Check-in Date", "fieldname": "check_in", "fieldtype": "Datetime", "width": 150},
        {"label": "Check-out Date", "fieldname": "check_out", "fieldtype": "Datetime", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Total Guests", "fieldname": "no_of_guests", "fieldtype": "Int", "width": 120},
    ]

def get_data(filters):
    conditions = ""
    
    if filters.get("status"):
        conditions += f" AND status = '{filters['status']}'"
    if filters.get("guest"):
        conditions += f" AND guest = '{filters['guest']}'"
    
    query = f"""
        SELECT
            name, guest, room, booking_date, check_in, check_out, status, no_of_guests
        FROM `tabReservation`
        WHERE docstatus < 2 {conditions}
        ORDER BY booking_date DESC
    """
    
    return frappe.db.sql(query, as_dict=True)
