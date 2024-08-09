from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProductModel(db.Model):

    prod_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(100), nullable=False)
    prod_desc = db.Column(db.String(255), nullable=False)
    prod_brand = db.Column(db.String(50), nullable=False)
    prod_price = db.Column(db.Integer, nullable=False)
    prod_img = db.Column(db.String(255), nullable=False, default='no_img.jpg')
    order_qty = db.Column(db.Integer, nullable=False)
    is_added_to_cart = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, desc, brand, price, img, order_qty=1, is_added_to_cart=False):
        self.prod_name = name
        self.prod_desc = desc
        self.prod_brand = brand
        self.prod_price = price
        self.prod_img = img
        self.order_qty = order_qty
        self.is_added_to_cart = is_added_to_cart

    def json(self):
        return (
            {'prodId': self.prod_id, 'prodName': self.prod_name, 'prodDesc': self.prod_desc, 'prodBrand': self.prod_brand,
             'prodPrice': self.prod_price, 'prodImg': self.prod_img, 'orderQty': self.order_qty, 'isAddedToCart': self.is_added_to_cart})


class CartModel(db.Model):

    prod_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(100), nullable=False)
    prod_desc = db.Column(db.String(255), nullable=False)
    prod_brand = db.Column(db.String(50), nullable=False)
    prod_price = db.Column(db.Integer, nullable=False)
    prod_img = db.Column(db.String(255), nullable=False)
    order_qty = db.Column(db.Integer, nullable=False)
    is_added_to_cart = db.Column(db.Boolean, nullable=False)

    def __init__(self, prod_id, name, desc, brand, price, img, order_qty=1, is_added_to_cart=True):
        self.prod_id = prod_id
        self.prod_name = name
        self.prod_desc = desc
        self.prod_brand = brand
        self.prod_price = price
        self.prod_img = img
        self.order_qty = order_qty
        self.is_added_to_cart = is_added_to_cart

    def json(self):
        return (
            {'prodId': self.prod_id, 'prodName': self.prod_name, 'prodDesc': self.prod_desc, 'prodBrand': self.prod_brand,
             'prodPrice': self.prod_price, 'prodImg': self.prod_img, 'orderQty': self.order_qty, 'isAddedToCart': self.is_added_to_cart})
