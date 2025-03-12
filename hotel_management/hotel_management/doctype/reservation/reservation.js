frappe.ui.form.on("Reservation", {
    refresh: function (frm) {
        if (frm.doc.status !== "Cancelled") {
            frm.add_custom_button("Cancel Reservation", function () {
                frappe.confirm(
                    "Do you want to view the Sales Invoice before canceling?",
                    function () {
                        frappe.call({
                            method: "hotel_management.api.get_sales_invoice_for_reservation",
                            args: { reservation_name: frm.doc.name },
                            callback: function (r) {
                                if (r.message) {
                                    frappe.set_route("Form", "Sales Invoice", r.message);
                                } else {
                                    frappe.msgprint("No Sales Invoice found for this reservation.");
                                }
                            }
                        });
                    },
                    function () {
                        frappe.call({
                            method: "hotel_management.api.cancel_reservation",
                            args: { reservation_name: frm.doc.name },
                            callback: function (r) {
                                if (!r.exc) {
                                    frappe.msgprint("Reservation Cancelled.");
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }).addClass("btn-danger");
        }
    },

    validate: async function (frm) {  
        if (frm.is_new() && frm.doc.room) { // Only check for new reservations
            let response = await frappe.db.get_value("Item", frm.doc.room, "custom_room_status");
            
            if (response && response.custom_room_status && response.custom_room_status !== "Available") {
                frappe.msgprint(
                    __("Room is currently {0}. Please choose a different room.", [response.custom_room_status])
                );
                frappe.validated = false;  // Prevent saving
            }
        }
    }
});
