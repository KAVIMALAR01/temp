frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {  
        frm.add_custom_button(__('Get Sales Order'), function() {
            let sales_orders = [];

            if (frm.doc.items && frm.doc.items.length > 0) {
                frm.doc.items.forEach(item => {
                    if (item.sales_order && !sales_orders.includes(item.sales_order)) {
                        sales_orders.push(item.sales_order);
                    }
                });
            }

            if (sales_orders.length > 0) {
                frappe.msgprint({
                    title: __('Linked Sales Orders'),
                    indicator: 'green',  
                    message: `The following Sales Orders are linked:<br><b>${sales_orders.join(", ")}</b>`
                });
            } else {
                frappe.msgprint({
                    title: __('No Sales Order Found'),
                    indicator: 'red',  
                    message: "No Sales Order is linked to this Sales Invoice."
                });
            }
        });
    }
});
