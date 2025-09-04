-- Minimal Northwind-like schema subset
CREATE TABLE IF NOT EXISTS Categories (
  CategoryID INTEGER PRIMARY KEY,
  CategoryName TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Customers (
  CustomerID TEXT PRIMARY KEY,
  CompanyName TEXT NOT NULL,
  Region TEXT
);

CREATE TABLE IF NOT EXISTS Products (
  ProductID INTEGER PRIMARY KEY,
  ProductName TEXT NOT NULL,
  CategoryID INTEGER,
  FOREIGN KEY(CategoryID) REFERENCES Categories(CategoryID)
);

CREATE TABLE IF NOT EXISTS Orders (
  OrderID INTEGER PRIMARY KEY,
  CustomerID TEXT,
  OrderDate TEXT,
  ShipRegion TEXT,
  FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE IF NOT EXISTS OrderDetails (
  OrderID INTEGER,
  ProductID INTEGER,
  UnitPrice REAL,
  Quantity INTEGER,
  Discount REAL DEFAULT 0,
  PRIMARY KEY (OrderID, ProductID),
  FOREIGN KEY(OrderID) REFERENCES Orders(OrderID),
  FOREIGN KEY(ProductID) REFERENCES Products(ProductID)
);

-- Seed minimal data
INSERT OR IGNORE INTO Categories(CategoryID, CategoryName) VALUES
  (1, 'Beverages'), (2, 'Condiments');

INSERT OR IGNORE INTO Customers(CustomerID, CompanyName, Region) VALUES
  ('ALFKI', 'Alfreds Futterkiste', 'Europe'),
  ('ANATR', 'Ana Trujillo Emparedados y helados', 'Americas');

INSERT OR IGNORE INTO Products(ProductID, ProductName, CategoryID) VALUES
  (1, 'Chai', 1), (2, 'Chang', 1), (3, 'Aniseed Syrup', 2);

INSERT OR IGNORE INTO Orders(OrderID, CustomerID, OrderDate, ShipRegion) VALUES
  (10248, 'ALFKI', '1996-07-04', 'Europe'),
  (10249, 'ANATR', '1996-07-05', 'Americas');

INSERT OR IGNORE INTO OrderDetails(OrderID, ProductID, UnitPrice, Quantity, Discount) VALUES
  (10248, 1, 18.0, 12, 0.0),
  (10248, 2, 19.0, 10, 0.05),
  (10249, 3, 10.0, 5, 0.0);
