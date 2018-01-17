# Copyright (c) 2013, Syed Abdul Qadeer and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext.controllers.queries import get_match_cond
from frappe import _

def execute(filters=None):
	if not filters: filters = frappe._dict()
	columns, data = get_data(frappe._dict(filters))
	return columns, data

def get_data(filters):
	conditions = ""
	if filters.from_date:
		conditions += " and `tabSales Invoice`.posting_date >= %(from_date)s"
	if filters.to_date:
		conditions += " and `tabSales Invoice`.posting_date <= %(to_date)s"

	columns = [_("Sales Invoice") + ":Link/Sales Invoice:120",
			_("Posting Date") + ":Date:120",
			_("Mode Of Payment") + "::120",
			_("Customer") + ":Link/Customer:120",
			_("City") + "::120",
			_("Country") + "::120",
			_("Postal Code") + "::120",
			_("Address") + "::120",
			_("Tax ID") + "::120",
			_("Total") + "::120",
			_("Tax") + "::120",
			_("Grand Total") + "::120"]

	if not filters.from_date and not filters.to_date:
		frappe.throw(_("Please select From Date and To Date"))

	data = frappe.db.sql("""
		SELECT
		`tabSales Invoice`.name,
		`tabSales Invoice`.posting_date,
		`tabSales Invoice`.mode_of_payment,
		`tabSales Invoice`.customer,
		`tabAddress`.city,
		`tabAddress`.country,
		`tabAddress`.pincode,
		`tabAddress`.address_line1,
		`tabSales Invoice`.tax_id,
		`tabSales Invoice`.total,
		CONCAT(ROUND((`tabSales Invoice`.total_taxes_and_charges / `tabSales Invoice`.total * 100), 2), "%%"),
		`tabSales Invoice`.grand_total
		
	FROM
		`tabSales Invoice` LEFT JOIN `tabAddress`
	ON `tabSales Invoice`.customer_address = `tabAddress`.name
	WHERE
		`tabSales Invoice`.docstatus = 1 {conditions} {match_cond}
	ORDER BY
		`tabSales Invoice`.posting_date desc, `tabSales Invoice`.posting_time desc
	""".format(conditions=conditions, match_cond = get_match_cond('Sales Invoice')), filters)
