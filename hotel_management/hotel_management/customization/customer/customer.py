import frappe
from frappe.model.document import Document
from datetime import datetime

class Customer(Document):
    def get_reservation_history(self):
        reservations = frappe.get_all(
            "Reservation",
            filters={"guest": self.name},
            fields=["name as reservation_id", "check_in", "check_out", "status"]
        )
        return reservations


def format_date(date):
    """Format datetime object as string or return 'N/A' if None."""
    return date.strftime("%Y-%m-%d %H:%M:%S") if date else "N/A"


def fetch_reservation_history(doc, method):
    """Fetch reservation history and store it in the custom_customer_history field."""
    reservations = frappe.get_all(
        "Reservation",
        filters={"guest": doc.name},
        fields=["name as reservation_id", "check_in", "check_out", "status"]
    )

    formatted_history = []
    for res in reservations:
        formatted_history.append(
            f"ID: {res['reservation_id']}, Status: {res['status']}, "
            f"Check-in: {format_date(res['check_in'])}, Check-out: {format_date(res['check_out'])}"
        )

    # Ensure the field exists before updating
    if hasattr(doc, "custom_customer_history"):
        doc.custom_customer_history = "\n".join(formatted_history) if formatted_history else "No reservations found."
