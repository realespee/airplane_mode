// Copyright (c) 2024, Simon Wanyama and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
        frm.trigger("make_website");
	},
    make_website(frm){
        const stream_link = frm.doc.website;
        frm.add_web_link(stream_link, "Visit Website");
    }
});
