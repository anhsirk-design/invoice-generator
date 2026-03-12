import tkinter as tk
from bill_logic import calculate_amount, calculate_total, clean_number, format_inr
from export_docx import export_bill
from export_pdf import convert_to_pdf
from datetime import date


class BillApp:

    def __init__(self, root):

        self.root = root
        root.title("Invoice Generator")
        root.bind("<Control-z>", lambda event: self.delete_last_item())

        self.items = []

        # Header fields
        tk.Label(root, text="Bill Number").pack()
        self.bill_entry = tk.Entry(root)
        self.bill_entry.pack()

        tk.Label(root, text="Client Name").pack()
        self.client_entry = tk.Entry(root)
        self.client_entry.pack()

        tk.Label(root, text="Invoice Date").pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, date.today().strftime("%d-%b-%Y"))
        self.date_entry.pack()

        tk.Label(root, text="Due Date").pack()
        self.due_entry = tk.Entry(root)
        self.due_entry.pack()

        # Item input
        tk.Label(root, text="Particulars").pack()
        self.desc_entry = tk.Entry(root, width=50)
        self.desc_entry.pack()

        tk.Label(root, text="Qty").pack()
        self.qty_entry = tk.Entry(root)
        self.qty_entry.pack()

        tk.Label(root, text="Rate").pack()
        self.rate_entry = tk.Entry(root)
        self.rate_entry.pack()

        tk.Button(root, text="Add Item", command=self.add_item).pack()
        tk.Button(root, text="Delete Last Item", command=self.delete_last_item).pack()

        # Item list
        self.items_box = tk.Listbox(root, width=70)
        self.items_box.pack()

        # Total
        self.total_label = tk.Label(root, text="Total: ₹0")
        self.total_label.pack()

        # Export buttons
        tk.Button(root, text="Export Word", command=self.export_word).pack()
        tk.Button(root, text="Export PDF", command=self.export_pdf).pack()

    def add_item(self):

        desc = self.desc_entry.get()
        qty = self.qty_entry.get()
        rate = clean_number(self.rate_entry.get())

        amount = calculate_amount(qty, rate)

        item = {
            "particulars": desc,
            "qty": qty,
            "rate": rate,
            "amount": amount
        }

        self.items.append(item)

        self.items_box.insert(
            tk.END,
            f"{desc} | Qty:{qty if qty else '-'} | Rate:{format_inr(rate)} | Amt:{format_inr(amount)}"
        )

        total = calculate_total([i["amount"] for i in self.items])
        self.total_label.config(text=f"Total: {format_inr(total)}")

        self.desc_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)

    def delete_last_item(self):
        if not self.items:
            return

        # remove last item from list
        self.items.pop()

        # remove last item from UI listbox
        self.items_box.delete(tk.END)

        # recalculate total
        total = calculate_total([i["amount"] for i in self.items])

        self.total_label.config(text=f"Total: {format_inr(total)}")

    def export_word(self):

        bill_no = self.bill_entry.get()
        client = self.client_entry.get()
        invoice_date = self.date_entry.get()
        due_date = self.due_entry.get()

        total = calculate_total([i["amount"] for i in self.items])

        export_bill(bill_no, client, self.items, total, due_date, invoice_date)

    def export_pdf(self):

        bill_no = self.bill_entry.get()
        client = self.client_entry.get()
        invoice_date = self.date_entry.get()
        due_date = self.due_entry.get()

        total = calculate_total([i["amount"] for i in self.items])

        docx_path = export_bill(bill_no, client, self.items, total, due_date, invoice_date)

        convert_to_pdf(docx_path)