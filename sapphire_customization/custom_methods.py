import frappe
from frappe.utils import flt, cint, cstr

def sales_order_negative_sales_alert(doc, method):
	"""
		Check if sales order has a negative sales
		if yes then send the notification to the user
	"""
	item_dict = {}
	for d in doc.items:
		cost_price = frappe.db.sql(""" select sum(rate)/2 from (
			select  pri.rate from `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pri 
			where pri.parent = pr.name 
				and item_code = '%(item_code)s' 
				and warehouse = '%(warehouse)s' 
			order by pr.modified desc 
			limit 2
		)foo """%{'item_code':d.item_code, 'warehouse':d.warehouse},as_list=1)

		if(d.rate < flt(cost_price[0][0])):
			item_dict.setdefault(d.item_code, {})
			item_dict[d.item_code]['item_code'] = d.item_code
			item_dict[d.item_code]['selling_price'] = d.rate
			item_dict[d.item_code]['buying_price'] = cost_price[0][0]
			item_dict[d.item_code]['qty'] = d.qty
			item_dict[d.item_code]['gross_margin'] = ((flt(d.rate) - flt(cost_price[0][0]) ) / flt(cost_price[0][0]))*100

		if item_dict:
			rows = ''
			rows1=''

			prof=frappe.db.sql("""select distinct name from tabUser p 
					where docstatus < 2 and enabled = 1 
					and name not in ("Administrator", "Guest") 
					and exists (select * from tabUserRole ur where ur.parent = p.name 
					and (ur.role="Alert Manager"))""",as_list=1)
			
			message = """  Sales Order %(name)s, for customer %(customer)s contains some items which are sold below cost price. 
				List of those items is as follow: <table>
						<tr>
							<th>Item Code</th>
							<th>Quantity</th>
							<th>Buying price</th>
							<th>Selling price</th>
							<th>Gross Margine</th>
						</tr>
					 %(rows)s  </table>"""

			tab_rows = """<tr>
						<td>%(item_code)s</td>
						<td>%(qty)s</td>
						<td>%(buying_price)s</td>
						<td>%(selling_price)s</td>
						<td>%(gross_margin)s</td>
					</tr>"""
			tab_rows1 = """<tr><td>%(item_code)s</td></tr>"""

			for item in item_dict:
				rows += tab_rows%item_dict[item]

			for item in item_dict:
				rows1 += tab_rows1%item_dict[item]

			b=frappe.session['user']
			query="select role from `tabUserRole` where role='System Manager' and parent ='"+b+"'"
			res=frappe.db.sql(query)
			if not res:
				frappe.msgprint("Sales Order have negative profit for follwing Items,\n %s\n Please contact 'System Manager' to submit this 'Sales Order'"%(rows1))
				raise Exception
			else:
				frappe.errprint(prof)
				if prof:
					frappe.sendmail([p[0] for p in prof], subject='Items sold below Cost Price', message=message%{'name':doc.name, 'customer': doc.customer, 'rows': rows})

def purchase_receipt_submit(doc, method):
	generate_warranty_code(doc)

def generate_warranty_code(doc):
	import string
	import random
	for item in doc.items:
		has_warranty_code=frappe.db.sql("""select has_warranty_code from tabItem where name='%s'"""%(item.item_code),as_dict=1)
		if has_warranty_code:
			if has_warranty_code[0]['has_warranty_code']=='Yes':
				if item.serial_no:
					serial_no=(item.serial_no).splitlines()
					for srno in serial_no:
						code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
						frappe.db.sql("""update `tabSerial No` set warranty_code='%s' where name='%s'"""%(code,srno))

@frappe.whitelist()
def get_invoice_info(sales_order):
	import json

	credit_limit=''
	credit_days=''
	tot_payment=0.0
	outstanding_exceeded=''
	doc = frappe.get_doc(json.loads(sales_order))
	customer = doc.customer
	
	credit_info=frappe.db.sql("""select credit_days,credit_limit from `tabCustomer` where name='%s'"""%(customer),as_dict=1)
	# todo add custom js and on customer trigger pass sales order doc
	if credit_info:
		credit_days=credit_info[0]['credit_days']
		credit_limit=credit_info[0]['credit_limit']

	outstanding_amount=frappe.db.sql("""select sum(coalesce(outstanding_amount,0)) as outstanding from `tabSales Invoice` where customer='%s' and docstatus = 1	and fiscal_year = %s"""%(customer,frappe.db.get_default("fiscal_year")),as_dict=1)

	if outstanding_amount:
		tot_payment=outstanding_amount[0]['outstanding']

	last_invoice=frappe.db.sql("""select creation, name,grand_total,mode_of_payment,outstanding_amount from `tabSales Invoice` where customer='%s' and docstatus=1 order by creation desc limit 10 """%(customer),as_dict=1)
	doc.set('transaction_details', [])
	
	for inv in last_invoice:
		ch = doc.append('transaction_details', {})
		ch.date = getdate(inv['creation'])
		ch.invoice_number = inv['name']
		ch.invoice_value = inv['grand_total']
		ageing=frappe.db.sql("""select DATEDIFF(now(),'%s') AS age"""%(inv['creation']),as_dict=1)
		
		if ageing:
			ch.payment_mode=ageing[0]['age']
		
		ch.outstanding_amount =inv['outstanding_amount']
		doc.save(ignore_permissions=True)
	
	outstanding_exceeded_info=frappe.db.sql("""select  sum(coalesce((select coalesce(outstanding_amount,0) from `tabSales Invoice` where name in (select parent from `tabSales Invoice Item` where sales_order=so.name) and DATE_ADD(creation,INTERVAL coalesce(so.period,0) day)>now() ),0)) as outstanding_amount  from `tabSales Order` so  where so.customer_name='%s'"""%(customer),as_dict=1)	
	
	if outstanding_exceeded_info:
		outstanding_exceeded=outstanding_exceeded_info[0]['outstanding_amount']

		return {
			"period":credit_days,
			"credit_limit":credit_limit,
			"total_outstanding_payment":tot_payment,
			"exceeded_amount":outstanding_exceeded
		}
