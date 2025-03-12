frappe.ui.form.on('Purchase Order', {
    refresh: function(frm) {
        frm.add_custom_button('Open Dialog', function() {
            let dialog = new frappe.ui.Dialog({
                title: 'Enter Details',
                fields: [
                    {
                        label: 'Enter Text',
                        fieldname: 'sample_text',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    {
                        label: 'Select Option',
                        fieldname: 'sample_option',
                        fieldtype: 'Select',
                        options: ['Option 1', 'Option 2', 'Option 3']
                    }
                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    frappe.msgprint({
                        title: 'Input Received',
                        message: `You entered: <b>${values.sample_text}</b><br>Selected: <b>${values.sample_option || 'None'}</b>`,
                        indicator: 'green'
                    });
                    dialog.hide();
                }
            });

            dialog.show();
        });
    }
});
