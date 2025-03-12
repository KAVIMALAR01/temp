frappe.ui.form.on('Purchase Invoice', {
    onload: function(frm) {
        frappe.msgprint('Purchase Invoice form has been loaded.');
    },

    refresh: function(frm) {
        frm.add_custom_button('Validate Invoice', function() {
            frappe.msgprint('Invoice validation started...');
        });
    },

    before_save: function(frm) {
        frappe.msgprint('Purchase Invoice is about to be saved.');
    },

    after_save: function(frm) {
        frappe.msgprint(`Purchase Invoice ${frm.doc.name} has been saved successfully.........`);
    },

   
    before_submit: function(frm) {
        frappe.msgprint('Purchase Invoice is about to be submitted...........');
    },

    on_submit: function(frm) {
        frappe.msgprint(`Purchase Invoice ${frm.doc.name} has been submitted........`);
    },

    before_cancel: function(frm) {
        frappe.throw('Are you sure you want to cancel this Purchase Invoice?');
    },

    
    on_cancel: function(frm) {
        frappe.msgprint(`Purchase Invoice ${frm.doc.name} has been canceled.`);
    },

    
    supplier: function(frm) {
        frappe.msgprint(`Supplier changed to: ${frm.doc.supplier}`);
    },

    
    validate: function(frm) {
        if (frm.doc.grand_total <= 0) {
            frappe.throw('Grand Total must be greater than zero.');
        }
    }
});
