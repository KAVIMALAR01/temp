frappe.listview_settings['Item'] = {
    add_fields: ["custom_room_status"], // Ensure this matches the fieldname
    get_indicator: function (doc) {
        if (doc.custom_room_status === "Available") {
            return ["Available", "green", "custom_room_status,=,Available"];
        } else if (doc.custom_room_status === "Booked") {
            return ["Booked", "red", "custom_room_status,=,Booked"];
        } else if (doc.custom_room_status === "Checked-in") {
            return ["Checked-in", "blue", "custom_room_status,=,Checked-in"];
        } else if (doc.custom_room_status === "Under Maintenance") {
            return ["Under Maintenance", "orange", "custom_room_status,=,Under Maintenance"];
        }
    }
};
