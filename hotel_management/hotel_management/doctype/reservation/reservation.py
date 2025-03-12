import frappe
from frappe.model.document import Document
from datetime import datetime
import math

class Reservation(Document):
    def before_save(self):
        self._validate_reservation_dates()
        self._validate_and_update_room_status()
        self._handle_deposit_invoice()
    
    def before_submit(self):
        """Ensure the deposit invoice is fully paid before allowing submission."""
        existing_invoice = frappe.get_all("Sales Invoice", filters={"custom_reservation": self.name}, fields=["name", "status"])

        if existing_invoice:
            invoice_status = existing_invoice[0]["status"]
            if invoice_status != "Paid":
                frappe.throw(f"Reservation cannot be submitted until the Sales Invoice <b>{existing_invoice[0]['name']}</b> is fully paid.")

    def on_update_after_submit(self):
        self._validate_and_update_room_status()
        self._handle_final_invoice()
        self._create_service_task_on_checkout() 

    def _validate_reservation_dates(self):
        """Ensure valid reservation dates and prevent overlapping reservations."""
        if not self.check_in or not self.check_out:
            frappe.throw("Both Check-in and Check-out dates are required.")

        check_in = datetime.strptime(str(self.check_in), "%Y-%m-%d %H:%M:%S")
        check_out = datetime.strptime(str(self.check_out), "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()

        if check_out <= check_in:
            frappe.throw("Check-out date must be after Check-in date.")

        if self.status != "Checked-in" and check_in < current_time:
            frappe.throw("Check-in date cannot be in the past.")

        overlapping_reservations = frappe.get_all(
            "Reservation",
            filters={
                "room": self.room,
                "status": ["in", ["Pending", "Confirmed", "Checked-in"]],
                "name": ["!=", self.name],
                "check_in": ["<", self.check_out],
                "check_out": [">", self.check_in]
            },
            fields=["name"]
        )

        if overlapping_reservations:
            frappe.throw(f"Room is already booked during this period. Please select different dates.")

    def _validate_and_update_room_status(self):
        if self.has_value_changed("status"):
            self._validate_status_transition()
            self._prevent_status_change_if_cancelled()
            self._update_room_status()

    def _validate_status_transition(self):
        status_order = ["Pending", "Confirmed", "Checked-in", "Checked-out"]
        if self.get_doc_before_save():
            prev_status = self.get_doc_before_save().status

            if prev_status in ["Checked-out", "Cancelled"]:
              if self.status != prev_status:
                 frappe.throw(f"Cannot change status after <b>{prev_status}</b>. This reservation is finalized.")
            if prev_status != "Cancelled" and self.status != "Cancelled":
                prev_index = status_order.index(prev_status) if prev_status in status_order else -1
                new_index = status_order.index(self.status) if self.status in status_order else -1
                if new_index < prev_index:
                    frappe.throw(f"Cannot change status from <b>{prev_status}</b> back to <b>{self.status}</b>.")

    def _prevent_status_change_if_cancelled(self):
        if self.get_doc_before_save():
            prev_status = self.get_doc_before_save().status
            if prev_status == "Cancelled" and self.status != "Cancelled":
                frappe.throw(f"Cannot change status from <b>Cancelled</b> to <b>{self.status}</b>.")

    def _update_room_status(self):
        if self.room:
            room_doc = frappe.get_doc("Item", self.room)
            prev_room_status = room_doc.custom_room_status

            room_status_map = {
                "Confirmed": "Booked",
                "Checked-in": "Checked-in",
                "Checked-out": "Available",
                "Cancelled": "Available",
            }

            new_room_status = room_status_map.get(self.status)

            if new_room_status:
                room_doc.custom_room_status = new_room_status
                room_doc.save(ignore_permissions=True)
                if prev_room_status != new_room_status:
                    frappe.msgprint(f"Room <b>{self.room}</b> status updated from <b>{prev_room_status}</b> to <b>{new_room_status}</b>.", title="Room Status Updated", indicator="green")

    def _handle_deposit_invoice(self):
        """Create Sales Invoice for deposit when status is set to Confirmed."""
        if self.status == "Confirmed" and (self.deposit_amount or 0) > 0:
            existing_invoice = frappe.get_all("Sales Invoice", filters={"custom_reservation": self.name}, fields=["name", "status"])
            
            if not existing_invoice:
                invoice = frappe.get_doc({
                    "doctype": "Sales Invoice",
                    "customer": self.guest,
                    "custom_reservation": self.name,
                    "custom_is_deposit": 1, 
                    "items": [{
                        "item_code": self.room,
                        "qty": 1,
                        "rate": self.deposit_amount,
                        "amount": self.deposit_amount
                    }],
                    "grand_total": self.deposit_amount,
                    "outstanding_amount": self.deposit_amount
                })
                invoice.insert(ignore_permissions=True)
                invoice.submit()
                frappe.msgprint(f"Sales Invoice <b>{invoice.name}</b> created for Deposit Amount of <b>₹{self.deposit_amount}</b>.")

    def _handle_final_invoice(self):
        """Create final Sales Invoice when reservation is checked out."""
        if self.status == "Checked-out":
            if frappe.db.exists("Sales Invoice", {"custom_reservation": self.name, "custom_is_deposit": 0}):
                frappe.msgprint("Final Sales Invoice already exists for this reservation.")
                return

            room_price = frappe.db.get_value("Item", self.room, "custom_standard_price") or 0

            check_in = datetime.strptime(str(self.check_in), "%Y-%m-%d %H:%M:%S")
            check_out = datetime.strptime(str(self.check_out), "%Y-%m-%d %H:%M:%S")

            num_nights = math.ceil((check_out - check_in).total_seconds() / (24 * 60 * 60))
            total_price = num_nights * room_price

            # Check if deposit is paid and deduct from total price
            deposit_invoice = frappe.get_all("Sales Invoice", filters={"custom_reservation": self.name, "custom_is_deposit": 1, "status": "Paid"}, fields=["grand_total"])
            deposit_paid = deposit_invoice[0]["grand_total"] if deposit_invoice else 0
            final_amount_due = total_price - deposit_paid
            #final_amount_due = total_price - self.total_amount
            sales_invoice = frappe.get_doc({
                "doctype": "Sales Invoice",
                "customer": self.guest,
                "custom_reservation": self.name,
                "items": [{
                    "item_code": self.room,
                    "qty": num_nights,
                    "rate": room_price,
                    "amount": final_amount_due
                }],
                "grand_total": total_price,
                "outstanding_amount": final_amount_due
            })
            sales_invoice.insert(ignore_permissions=True)
            frappe.msgprint(f"Sales Invoice <b>{sales_invoice.name}</b> created with total charge ₹{total_price} for {num_nights} nights. Deposit of ₹{deposit_paid} applied. Amount due: ₹{final_amount_due}")
    
    def _create_service_task_on_checkout(self):
        """Create a Task for cleaning/maintenance when the reservation is checked out."""
        if self.status == "Checked-out":
            task_exists = frappe.db.exists("Task", {"custom_reservation": self.name})
            if task_exists:
                frappe.msgprint(f"A service task already exists for Reservation <b>{self.name}</b>.", indicator="yellow")
                return
            
            # Get available employee
            available_employee = frappe.get_value("Employee", {"status": "Active","department": "House Keeping - I"}, "name")

            task = frappe.get_doc({
                "doctype": "Task",
                "subject": f"Cleaning Service - Room {self.room}",
                "custom_reservation": self.name,
                "custom_room": self.room,
                "custom_service_type": "Cleaning",
                "custom_assigned_to": available_employee if available_employee else None,
                "status": "Open",
                "expected_end_date": frappe.utils.add_days(frappe.utils.today(), 1),
                "description": f"Cleaning required for Room {self.room} after guest check-out."
            })
            task.insert(ignore_permissions=True)
            frappe.msgprint(f"Service Task <b>{task.name}</b> created for Room <b>{self.room}</b> after check-out.", indicator="green")
