-- ==========================================
-- Customer Table
-- ==========================================

CREATE TABLE IF NOT EXISTS Customer (
customer_id INT PRIMARY KEY,
customer_name VARCHAR(100) NOT NULL,
email VARCHAR(100)
);

-- ==========================================
-- Account Table
-- ==========================================

CREATE TABLE IF NOT EXISTS Account (
account_id INT PRIMARY KEY,
customer_id INT NOT NULL,
account_type VARCHAR(50),
balance DECIMAL(12,2),

```
CONSTRAINT fk_customer
FOREIGN KEY (customer_id)
REFERENCES Customer(customer_id)
```

);

-- ==========================================
-- Transaction Table
-- ==========================================

CREATE TABLE IF NOT EXISTS TransactionTable (
transaction_id INT PRIMARY KEY,
account_id INT NOT NULL,
amount DECIMAL(12,2),
transaction_date DATE,

```
CONSTRAINT fk_account
FOREIGN KEY (account_id)
REFERENCES Account(account_id)
```

);

-- ==========================================
-- Sample Customers
-- ==========================================

INSERT INTO Customer
(customer_id, customer_name, email)
VALUES
(101, 'John Doe', '[john@example.com](mailto:john@example.com)'),
(102, 'Alice Smith', '[alice@example.com](mailto:alice@example.com)'),
(103, 'Robert Brown', '[robert@example.com](mailto:robert@example.com)');

-- ==========================================
-- Sample Accounts
-- ==========================================

INSERT INTO Account
(account_id, customer_id, account_type, balance)
VALUES
(1001, 101, 'Savings', 50000),
(1002, 101, 'Current', 25000),
(1003, 102, 'Savings', 40000),
(1004, 103, 'Current', 30000);

-- ==========================================
-- Sample Transactions
-- ==========================================

INSERT INTO TransactionTable
(transaction_id, account_id, amount, transaction_date)
VALUES

(1, 1001, 5000, '2025-01-05'),
(2, 1001, 3000, '2025-01-10'),
(3, 1002, 2000, '2025-01-15'),

(4, 1003, 7000, '2025-01-20'),
(5, 1003, 1500, '2025-01-25'),

(6, 1004, 4000, '2025-01-28'),

(7, 1001, 2500, '2025-02-05'),
(8, 1002, 1800, '2025-02-10'),
(9, 1003, 3200, '2025-02-12');
