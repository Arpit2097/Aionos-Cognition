SALES_BY_REGION = (
    "SELECT COALESCE(ShipRegion, 'Unknown') AS label, "
    "ROUND(SUM((UnitPrice * Quantity) * (1 - Discount)), 2) AS value "
    "FROM Orders o JOIN OrderDetails od ON o.OrderID = od.OrderID "
    "GROUP BY ShipRegion ORDER BY value DESC"
)

SALES_BY_CATEGORY = (
    "SELECT c.CategoryName AS label, "
    "ROUND(SUM((od.UnitPrice * od.Quantity) * (1 - od.Discount)), 2) AS value "
    "FROM Categories c JOIN Products p ON p.CategoryID = c.CategoryID "
    "JOIN OrderDetails od ON od.ProductID = p.ProductID "
    "GROUP BY c.CategoryName ORDER BY value DESC"
)

