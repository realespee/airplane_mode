// Copyright (c) 2024, Simon Wanyama and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	refresh(frm) {
        frm.trigger("add_assign_gate_number_button");
	},
    add_assign_gate_number_button: function (frm) {
        frm.add_custom_button(__('Assign Gate Number'), function () {
            frm.trigger('assign_gate_number_dialog')
        }).removeClass('btn-default').addClass('btn-primary');
    },
    assign_gate_number_dialog: function (frm) {
        var d = new frappe.ui.Dialog({
            title: 'Select Gate Number',
            fields: [
                {
                    label: 'Gate Number',
                    fieldname: 'gate_number',
                    fieldtype: 'Data',
                    reqd: 1
                }
            ],
            primary_action_label: 'Assign',
            primary_action: function (data) {
                frm.set_value('gate_number', data.gate_number);
                frm.save_or_update()
                d.hide();
            }
        });
        d.show();
    }
});
