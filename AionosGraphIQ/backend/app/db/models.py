from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey, Date

Base = declarative_base()

class Category(Base):
    __tablename__ = "Categories"
    CategoryID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CategoryName: Mapped[str] = mapped_column(String, nullable=False)
    products = relationship("Product", back_populates="category")

class Customer(Base):
    __tablename__ = "Customers"
    CustomerID: Mapped[str] = mapped_column(String, primary_key=True)
    CompanyName: Mapped[str] = mapped_column(String, nullable=False)
    Region: Mapped[str | None] = mapped_column(String, nullable=True)
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = "Products"
    ProductID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ProductName: Mapped[str] = mapped_column(String, nullable=False)
    CategoryID: Mapped[int | None] = mapped_column(Integer, ForeignKey("Categories.CategoryID"))
    category = relationship("Category", back_populates="products")
    order_details = relationship("OrderDetail", back_populates="product")

class Order(Base):
    __tablename__ = "Orders"
    OrderID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CustomerID: Mapped[str | None] = mapped_column(String, ForeignKey("Customers.CustomerID"))
    OrderDate: Mapped[Date | None] = mapped_column(Date, nullable=True)
    ShipRegion: Mapped[str | None] = mapped_column(String, nullable=True)
    customer = relationship("Customer", back_populates="orders")
    details = relationship("OrderDetail", back_populates="order")

class OrderDetail(Base):
    __tablename__ = "OrderDetails"
    OrderID: Mapped[int] = mapped_column(Integer, ForeignKey("Orders.OrderID"), primary_key=True)
    ProductID: Mapped[int] = mapped_column(Integer, ForeignKey("Products.ProductID"), primary_key=True)
    UnitPrice: Mapped[float] = mapped_column(Float, nullable=False)
    Quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    Discount: Mapped[float] = mapped_column(Float, default=0.0)
    order = relationship("Order", back_populates="details")
    product = relationship("Product", back_populates="order_details")
