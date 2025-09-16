from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QVBoxLayout, QCheckBox
)

class CustomerForm(QDialog):
    def __init__(self, parent=None, customer_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Customer")

        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()

        self.fields = {
            "coid": QLineEdit(),
            "company_name": QLineEdit(),
            "short_name": QLineEdit(),
            "contact_person": QLineEdit(),
            "phone": QLineEdit(),
            "email": QLineEdit(),
            "address_line1": QLineEdit(),
            "address_line2": QLineEdit(),
            "city": QLineEdit(),
            "state": QLineEdit(),
            "postal_code": QLineEdit(),
            "country": QLineEdit(),
            "is_active": QCheckBox("Active")
        }

        for label, widget in self.fields.items():
            self.form_layout.addRow(label.replace("_", " ").title(), widget)

        self.layout.addLayout(self.form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

        if customer_data:
            self.populate_form(customer_data)

    def populate_form(self, customer_data):
        # The customer_data comes from the database as a tuple (pyodbc.Row)
        # The order of fields is: id, coid, company_name, ...
        self.fields["coid"].setText(str(customer_data[1]))
        self.fields["company_name"].setText(str(customer_data[2]))
        self.fields["short_name"].setText(str(customer_data[3]))
        self.fields["contact_person"].setText(str(customer_data[4]))
        self.fields["phone"].setText(str(customer_data[5]))
        self.fields["email"].setText(str(customer_data[6]))
        self.fields["address_line1"].setText(str(customer_data[7]))
        self.fields["address_line2"].setText(str(customer_data[8]))
        self.fields["city"].setText(str(customer_data[9]))
        self.fields["state"].setText(str(customer_data[10]))
        self.fields["postal_code"].setText(str(customer_data[11]))
        self.fields["country"].setText(str(customer_data[12]))
        self.fields["is_active"].setChecked(bool(customer_data[13]))

    def get_form_data(self):
        return {
            "coid": self.fields["coid"].text(),
            "company_name": self.fields["company_name"].text(),
            "short_name": self.fields["short_name"].text(),
            "contact_person": self.fields["contact_person"].text(),
            "phone": self.fields["phone"].text(),
            "email": self.fields["email"].text(),
            "address_line1": self.fields["address_line1"].text(),
            "address_line2": self.fields["address_line2"].text(),
            "city": self.fields["city"].text(),
            "state": self.fields["state"].text(),
            "postal_code": self.fields["postal_code"].text(),
            "country": self.fields["country"].text(),
            "is_active": self.fields["is_active"].isChecked()
        }
