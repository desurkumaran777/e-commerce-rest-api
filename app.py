from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import os

from models import ProductModel, db, CartModel

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(file_name):
    return ('.' in file_name) and (file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


api = Api(app)
db.init_app(app)


class ProductsView(Resource):
    def get(self):
        products = ProductModel.query.all()
        return {'Products': list(prod.json() for prod in products)}, 200

    def post(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files.get('file')
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            file.save(file_path)

            data = request.form
            new_prod = ProductModel(data.get('prodName'), data.get(
                'prodDesc'), data.get('prodBrand'), data.get('prodPrice'), file_name)
            db.session.add(new_prod)
            db.session.commit()
            print('it is added to db')
            return new_prod.json(), 201
        else:
            return jsonify({'error': 'File type not allowed'}), 400


class ProductView(Resource):
    def get(self, prod_id):
        product = ProductModel.query.get_or_404(prod_id)
        return product.json(), 200

    def delete(self, prod_id):
        product = ProductModel.query.get_or_404(prod_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'deleted successfully'}

    def put(self, prod_id):
        data = request.get_json()
        product = ProductModel.query.filter_by(prod_id=prod_id).first()
        if product:
            product.prod_name = data.get('prodName')
            product.prod_desc = data.get('prodDesc')
            product.prod_brand = data.get('prodBrand')
            product.prod_price = data.get('prodPrice')
            product.order_qty = data.get('orderQty')
            product.is_added_to_cart = data.get('isAddedToCart')
            db.session.commit()
            return product.json(), 200

        else:
            return jsonify({'message': 'Product not found'}), 404


class CartsView(Resource):
    def get(self):
        products = CartModel.query.all()
        return {'Carts': list(prod.json() for prod in products)}, 200

    def post(self):
        data = request.get_json()
        new_prod = CartModel(data.get('prodId'), data.get('prodName'), data.get(
            'prodDesc'), data.get('prodBrand'), data.get('prodPrice'), data.get('prodImg'))
        db.session.add(new_prod)
        db.session.commit()
        return new_prod.json(), 201


class CartView(Resource):
    def get(self, prod_id):
        product = CartModel.query.get_or_404(prod_id)
        return product.json(), 200

    def delete(self, prod_id):
        product = CartModel.query.get_or_404(prod_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'deleted successfully'}

    def put(self, prod_id):
        data = request.get_json()
        product = CartModel.query.filter_by(prod_id=prod_id).first()
        if product:
            product.prod_name = data.get('prodName')
            product.prod_desc = data.get('prodDesc')
            product.prod_brand = data.get('prodBrand')
            product.prod_price = data.get('prodPrice')
            product.order_qty = data.get('orderQty')
            product.is_added_to_cart = data.get('isAddedToCart')
            db.session.commit()
            return product.json(), 200

        else:
            return {'message': 'cart is not found'}, 404


class ImageServe(Resource):
    def get(self, file_name):
        return send_from_directory(app.config['UPLOAD_FOLDER'], file_name)


api.add_resource(ProductsView, '/products')
api.add_resource(ProductView, '/product/<int:prod_id>')
api.add_resource(CartsView, '/carts')
api.add_resource(CartView, '/cart/<int:prod_id>')
api.add_resource(ImageServe, '/image/<string:file_name>')

app.debug = True

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=5000)
