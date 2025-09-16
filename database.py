import pyodbc

class Database:
    def __init__(self):
        # NOTE: Please replace the placeholder credentials with your actual
        # MSSQL database connection details.
        self.conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=your_server_name;'
            r'DATABASE=your_database_name;'
            r'UID=your_username;'
            r'PWD=your_password;'
        )
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.conn_str)
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Database connection error: {sqlstate}")
            # In a real application, you might want to handle this more gracefully,
            # perhaps by showing an error message to the user.
            self.conn = None

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def fetch_all_customers(self):
        if not self.conn:
            return []
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, coid, company_name, short_name, contact_person, phone, email, address_line1, address_line2, city, state, postal_code, country, is_active, date_created, date_updated FROM customers")
        rows = cursor.fetchall()
        return [row for row in rows]

    def add_customer(self, customer_data):
        if not self.conn:
            return False
        cursor = self.conn.cursor()
        sql = """
            INSERT INTO customers (
                coid, company_name, short_name, contact_person, phone, email,
                address_line1, address_line2, city, state, postal_code, country,
                is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(sql, tuple(customer_data.values()))
            self.conn.commit()
            return True
        except pyodbc.Error as ex:
            print(f"Error adding customer: {ex}")
            self.conn.rollback()
            return False

    def update_customer(self, customer_id, customer_data):
        if not self.conn:
            return False
        cursor = self.conn.cursor()
        sql = """
            UPDATE customers SET
                coid = ?, company_name = ?, short_name = ?, contact_person = ?,
                phone = ?, email = ?, address_line1 = ?, address_line2 = ?,
                city = ?, state = ?, postal_code = ?, country = ?, is_active = ?
            WHERE id = ?
        """
        try:
            params = list(customer_data.values())
            params.append(customer_id)
            cursor.execute(sql, tuple(params))
            self.conn.commit()
            return True
        except pyodbc.Error as ex:
            print(f"Error updating customer: {ex}")
            self.conn.rollback()
            return False

    def delete_customer(self, customer_id):
        if not self.conn:
            return False
        cursor = self.conn.cursor()
        sql = "DELETE FROM customers WHERE id = ?"
        try:
            cursor.execute(sql, customer_id)
            self.conn.commit()
            return True
        except pyodbc.Error as ex:
            print(f"Error deleting customer: {ex}")
            self.conn.rollback()
            return False
