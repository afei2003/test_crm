import sys
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout, QMessageBox, QHeaderView
)
from database import Database
from customer_form import CustomerForm

class CustomerTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Format boolean values for display
            value = self._data[index.row()][index.column()]
            if isinstance(value, bool):
                return "Yes" if value else "No"
            return value
        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

    def update_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Management")
        self.db = Database()

        # Main layout
        layout = QVBoxLayout()

        # Table view
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_view)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Customer")
        self.edit_button = QPushButton("Edit Customer")
        self.delete_button = QPushButton("Delete Customer")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        # Connect buttons to functions
        self.add_button.clicked.connect(self.add_customer)
        self.edit_button.clicked.connect(self.edit_customer)
        self.delete_button.clicked.connect(self.delete_customer)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Load data
        self.load_customers()

    def load_customers(self):
        customers = self.db.fetch_all_customers()
        headers = [
            "ID", "COID", "Company Name", "Short Name", "Contact", "Phone",
            "Email", "Address 1", "Address 2", "City", "State",
            "Postal Code", "Country", "Active", "Created", "Updated"
        ]

        if not self.db.conn: # Check if the database connection failed
            customers = [
                (1, 'C001', 'Company A', 'CA', 'John Doe', '123-456-7890', 'john.doe@companya.com', '123 Main St', '', 'Anytown', 'Anystate', '12345', 'USA', True, '2023-01-01', '2023-01-01'),
                (2, 'C002', 'Company B', 'CB', 'Jane Smith', '098-765-4321', 'jane.smith@companyb.com', '456 Oak Ave', '', 'Someville', 'Somestate', '54321', 'USA', True, '2023-01-02', '2023-01-02')
            ]

        customers_as_list = [tuple(row) for row in customers]

        if not hasattr(self, 'model'):
            self.model = CustomerTableModel(customers_as_list, headers)
            self.proxy_model = QSortFilterProxyModel()
            self.proxy_model.setSourceModel(self.model)
            self.table_view.setModel(self.proxy_model)
        else:
            self.model.update_data(customers_as_list)

    def add_customer(self):
        form = CustomerForm(self)
        if form.exec():
            customer_data = form.get_form_data()
            if self.db.add_customer(customer_data):
                self.load_customers()
            else:
                QMessageBox.critical(self, "Error", "Failed to add customer.")

    def edit_customer(self):
        selected_proxy_row = self.table_view.selectionModel().currentIndex()
        if not selected_proxy_row.isValid():
            QMessageBox.warning(self, "Warning", "Please select a customer to edit.")
            return

        selected_source_row = self.proxy_model.mapToSource(selected_proxy_row)
        customer_data = self.model._data[selected_source_row.row()]
        customer_id = customer_data[0]

        form = CustomerForm(self, customer_data=customer_data)
        if form.exec():
            new_customer_data = form.get_form_data()
            if self.db.update_customer(customer_id, new_customer_data):
                self.load_customers()
            else:
                QMessageBox.critical(self, "Error", "Failed to update customer.")

    def delete_customer(self):
        selected_proxy_row = self.table_view.selectionModel().currentIndex()
        if not selected_proxy_row.isValid():
            QMessageBox.warning(self, "Warning", "Please select a customer to delete.")
            return

        selected_source_row = self.proxy_model.mapToSource(selected_proxy_row)
        customer_data = self.model._data[selected_source_row.row()]
        customer_id = customer_data[0]
        company_name = customer_data[2]

        reply = QMessageBox.question(
            self, "Delete Customer",
            f"Are you sure you want to delete '{company_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.db.delete_customer(customer_id):
                self.load_customers()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete customer.")

    def closeEvent(self, event):
        self.db.disconnect()
        event.accept()
