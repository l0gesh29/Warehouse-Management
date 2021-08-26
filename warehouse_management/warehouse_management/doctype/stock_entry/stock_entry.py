# Copyright (c) 2021, Logesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StockEntry(Document):
    def on_submit(self):
        if self.type == 'Add':
            warehouse_doc = frappe.get_doc('Warehouse', self.warehouse)
            item_exist = frappe.db.get_value('Warehouse Item', {'item': self.item, 'parent':self.warehouse})
            if item_exist:
                qty = frappe.db.get_value('Warehouse Item', {'item': self.item, 'parent':self.warehouse}, 'qty')
                frappe.db.set_value('Warehouse Item', {'item': self.item, 'parent':self.warehouse}, 'qty', qty + self.quantity)
                frappe.msgprint("Item Added")
            else:
                warehouse_doc.append('warehouse_item',{'item': self.item, 'qty': self.quantity})
                warehouse_doc.save()
        if self.type == 'Remove':
            warehouse_doc = frappe.get_doc('Warehouse', self.warehouse)
            item_exist = frappe.db.get_value('Warehouse Item', {'item': self.item, 'parent':self.warehouse})
            print(item_exist)
            if item_exist:
                qty = frappe.db.get_value('Warehouse Item', {'item': self.item, 'parent':self.warehouse}, 'qty')
                current_quantity=qty - self.quantity
                frappe.db.set_value('Warehouse Item', {'item': self.item, 'parent':self.warehouse}, 'qty', current_quantity)
                if current_quantity==0:
                    for row in warehouse_doc.warehouse_item:
                        if row.item == self.item:
                            warehouse_doc.warehouse_item.remove(row)
                    for row in warehouse_doc.warehouse_item:
                        idx=0
                        row.idx=idx
                        idx+=1
                warehouse_doc.save()
                frappe.msgprint("Item Removed")
            else:
                frappe.throw("Item Not Found in the warehouse")
        if self.type == 'Move':
            warehouse_doc = frappe.get_doc('Warehouse', self.from_warehouse)
            item_exist = frappe.db.get_value('Warehouse Item', {'item': self.item, 'parent':self.from_warehouse})
            if item_exist:
                from_qty = frappe.db.get_value('Warehouse Item', {'item': self.item, 'parent':self.from_warehouse}, 'qty')
                to_qty = frappe.db.get_value('Warehouse Item', {'item': self.item, 'parent':self.to_warehouse}, 'qty')
                frappe.db.set_value('Warehouse Item', {'item': self.item, 'parent':self.to_warehouse}, 'qty', to_qty + self.quantity)
                frappe.db.set_value('Warehouse Item', {'item': self.item, 'parent':self.from_warehouse}, 'qty', from_qty - self.quantity)
            else:
                frappe.throw("Item Not Found in the warehouse")


@frappe.whitelist()
def get_quantity(warehouse,item):
    quantity=	frappe.db.get_value('Warehouse Item',{'parent':warehouse, 'item':item},'qty')
    return quantity