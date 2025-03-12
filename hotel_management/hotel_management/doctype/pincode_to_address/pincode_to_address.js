frappe.ui.form.on('Pincode to address', {
    refresh: function(frm) {
        if (!frm.custom_buttons_added) {  
            frm.custom_buttons_added = true;

            frm.add_custom_button(__('Get Address'), function() {
                if (!frm.doc.pincode) {
                    frappe.msgprint(__('Please enter a Pincode first.'));
                    return;
                }
                frappe.call({
                    method: "hotel_management.hotel_management.doctype.pincode_to_address.pincode_to_address.get_address_details",
                    args: { pincode: frm.doc.pincode },
                    callback: function(r) {
                        if (r.message && r.message.Status === "Success") {
                            let post_offices = r.message.PostOffice;
                            let address_text = "";

                            post_offices.forEach((office, index) => {
                                address_text += `${index + 1}. ${office.Name}, ${office.District}, ${office.State}, ${office.Country}\n`;
                            });

                            frm.set_value('address_details', address_text);

                            frappe.msgprint(__('Address details fetched successfully!'));
                        } else {
                            frappe.msgprint(__('Invalid Pincode or No records found.'));
                        }
                    }
                });
            }).addClass('btn-primary'); 
        }
    }
});
