class Invoice:
    def __init__(self, invoiceId, customerId, orderId, subtotal, tax, total, paymentMethodId):
        self.invoiceId = invoiceId
        self.customerId = customerId
        self.orderId = orderId
        self.subtotal = subtotal
        self.tax = tax
        self.total = total
        self.paymentMethodId = paymentMethodId

class Product:
    def __init__(self, productId, name, price):
        self.productId = productId
        self.name = name
        self.price = price
    
    def serialize(self):
        return {"productId":self.productId, "name":self.name, "price":self.price}

class StatsResponse:
    def __init__(self, topProduct, yearlyNumSales, yearlyRevenue, yearlyRevAvrg):
        self.topProduct = topProduct
        self.yearlySales = yearlyNumSales#Dictionaries like: {year:value}
        self.yearlyRevenue = yearlyRevenue
        self.yearlyRevAvrg = yearlyRevAvrg
    
    def serialize(self):
        return {"topProduct":self.topProduct.serialize(), "yearlySales":self.yearlySales, "yearlyRevenue":self.yearlyRevenue, "yearlyRevAvrg":self.yearlyRevAvrg}