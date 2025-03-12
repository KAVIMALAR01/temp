frappe.listview_settings['Reservation'] = {
    add_fields: ["status"], // Ensure this matches the fieldname in the Reservation Doctype
    get_indicator: function (doc) {
        if (doc.status === "Pending") {
            return ["Pending", "orange", "status,=,Pending"];
        } else if (doc.status === "Confirmed") {
            return ["Confirmed", "blue", "status,=,Confirmed"];
        } else if (doc.status === "Checked-in") {
            return ["Checked-in", "green", "status,=,Checked-in"];
        } else if (doc.status === "Checked-out") {
            return ["Checked-out", "gray", "status,=,Checked-out"];
        } else if (doc.status === "Cancelled") {
            return ["Cancelled", "red", "status,=,Cancelled"];
        }
    }
};
