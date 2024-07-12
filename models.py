from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProductModel(db.Model):
    __tablename__ = 'products'

    prod_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(100), nullable=False)
    prod_desc = db.Column(db.String(255), nullable=False)
    prod_brand = db.Column(db.String(50), nullable=False)
    prod_price = db.Column(db.Integer, nullable=False)
    order_qty = db.Column(db.Integer, nullable=False)
    is_added_to_cart = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, desc, brand, price, order_qty=1, is_added_to_cart=False):
        self.prod_name = name
        self.prod_desc = desc
        self.prod_brand = brand
        self.prod_price = price
        self.order_qty = order_qty
        self.is_added_to_cart = is_added_to_cart

    def json(self):
        return (
            {'prodId': self.prod_id, 'prodName': self.prod_name, 'prodDesc': self.prod_desc, 'prodBrand': self.prod_brand,
             'prodPrice': self.prod_price, 'orderQty': self.order_qty, 'isAddedToCart': self.is_added_to_cart})
