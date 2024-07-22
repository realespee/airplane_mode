// Copyright (c) 2024, Simon Wanyama and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Leasing Application", {
    
	refresh(frm) {
        if(frm.doc.status == "Applied" && !frm.is_new()){
            $(".primary-action").hide()
            frm.add_custom_button('Approve', () => {
                frappe.confirm('Approve this Application?',
                    () => {
                        frm.set_value("status", "Approved")
                        frm.save('Submit')
                    }, () => {
                        // action to perform if No is selected
                    })
                
            }).removeClass('btn-default').addClass('btn-success')
            frm.add_custom_button('Reject', () => {
                frappe.confirm('Are you sure you want to proceed?',
                    () => {
                        frm.set_value("status", "Rejected")
                        frm.save('Submit')
                    }, () => {
                        // action to perform if No is selected
                    })
                
            }).removeClass('btn-default').addClass('btn-danger')
        }else{
            $(".primary-action").show()
        }

        if(frm.doc.docstatus == 1) $('button[data-label="Cancel"]').hide();
	},
});
