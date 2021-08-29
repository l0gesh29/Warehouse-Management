// Copyright (c) 2021, Logesh and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Entry', {
	// refresh: function(frm) {

	// }
	//code
	item: function(frm){
	frm.set_value('available_quantity',0)
	if(frm.doc.type=="Move"){
		frappe.call({
			method: 'warehouse_management.warehouse_management.doctype.stock_entry.stock_entry.get_quantity',
			args: {
				'warehouse':frm.doc.from_warehouse,
				'item':frm.doc.item
			},
			callback: function(r) {
				if (r.message) {
					// code 
					frm.set_value('available_quantity',r.message)
					frm.refresh_fields();
				}
			}
		});
	}
		if(frm.doc.type=="Add" || frm.doc.type=="Remove"){
			frappe.call({
				method: 'warehouse_management.warehouse_management.doctype.stock_entry.stock_entry.get_qty',
				args: {
					'warehouse':frm.doc.warehouse,
					'item':frm.doc.item
				},
				callback: function(r) {
					if (r.message) {
						// code 
						frm.set_value('available_quantity',r.message)
						frm.refresh_fields();
					}
				}
			});
		}
	}
	
});
