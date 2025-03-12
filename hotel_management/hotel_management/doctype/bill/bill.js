// Copyright (c) 2025, Kavi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Bill", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Bill', {
    service_charges: function(frm) {
        update_total_amount(frm);
    },
    tax: function(frm) {
        update_total_amount(frm);
    }
});

function update_total_amount(frm) {
    let room_charges = frm.doc.room_charges || 0;
    let service_charges = frm.doc.service_charges || 0;
    let tax = frm.doc.tax || 0;

    // Calculate total amount
    let total_amount = room_charges + service_charges + tax;

    // Set the total amount
    frm.set_value('total_amount', total_amount);
}
