// Copyright (c) 2024, Simon Wanyama and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh: function (frm) {
        frm.trigger("add_assign_seat_button")
    },
    add_assign_seat_button: function (frm) {
        frm.add_custom_button(__('Assign Seat'), function () {
            frm.trigger('assign_seat_dialog')
        }).removeClass('btn-default').addClass('btn-primary');
    },
    assign_seat_dialog: function (frm) {
        var d = new frappe.ui.Dialog({
            title: 'Select Seat',
            fields: [
                {
                    label: 'Seat Number',
                    fieldname: 'seat_number',
                    fieldtype: 'Data',
                    reqd: 1
                }
            ],
            primary_action_label: 'Assign',
            primary_action: function (data) {
                frm.set_value('seat', data.seat_number);
                frm.save()
                d.hide();
            }
        });
        d.show();
    }
});

