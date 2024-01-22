import subprocess
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from flask_limiter import Limiter,util
app = Flask(__name__, instance_relative_config=True)
limiter = Limiter( 
    key_func=util.get_remote_address,
    app=app,
    default_limits=["6 per minute, 48 per hour"]
)
limiter.init_app(app)
CORS(app, origins="*")
# Load the file specified by the APP_CONFIG_FILE environment variable
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)

class ProductResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    img = db.Column(db.String(1000))
    url = db.Column(db.String(1000))
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    search_text = db.Column(db.String(255))
    source = db.Column(db.String(255))

    def __init__(self, name, img, url, price, search_text, source):
        self.name = name
        self.url = url
        self.img = img
        self.price = price
        self.search_text = search_text
        self.source = source


# class TrackedProducts(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(1000))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     tracked = db.Column(db.Boolean, default=True)

#     def __init__(self, name, tracked=True):
#         self.name = name
#         self.tracked = tracked

# receives data after scraping a browser page
# creates db objects
# saves them into db
@app.route('/results', methods=['POST'])
def submit_results():
    results = request.json.get('data')
    # print("****RESULTS")
    # print(results)
    search_text = request.json.get("search_text")
    source = request.json.get("source")

    for result in results:
        product_result = ProductResult(
            name=result['name'],
            url=result['url'],
            img=result["img"].split("?")[0],
            price=result['price'],
            search_text=search_text,
            source=source
        )
        db.session.add(product_result)

    db.session.commit()
    response = {'message': 'Received data successfully'}
    return jsonify(response), 200


@app.route('/unique_search_texts', methods=['GET'])
def get_unique_search_texts():
    unique_search_texts = db.session.query(
        ProductResult.search_text).distinct().all()
    unique_search_texts = [text[0] for text in unique_search_texts]
    return jsonify(unique_search_texts)

# TODO - enhance error reporting
@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="ratelimit exceeded", message=str(e.description)), 429


# called on selection from previous searched products
@app.route('/results')
def get_product_results():
    search_text = request.args.get('search_text')
    results = ProductResult.query.filter_by(search_text=search_text).order_by(
        ProductResult.created_at.desc()).all()
    

    product_dict = {}
    for result in results:
        url = result.url
        if url not in product_dict:
            product_dict[url] = {
                'name': result.name,
                'url': result.url,
                "img": result.img,
                "source": result.source,
                "created_at": result.created_at,
                'priceHistory': []
            }
        product_dict[url]['priceHistory'].append({
            'price': result.price,
            'date': result.created_at
        })

    formatted_results = list(product_dict.values())

    return jsonify(formatted_results)


@app.route('/all-results', methods=['GET'])
def get_results():
    results = ProductResult.query.all()
    product_results = []
    for result in results:
        product_results.append({
            'name': result.name,
            'url': result.url,
            'price': result.price,
            "img": result.img,
            'date': result.created_at,
            "created_at": result.created_at,
            "search_text": result.search_text,
            "source": result.source
        })

    return jsonify(product_results)

# route invoked by search button
@app.route('/start-scraper', methods=['POST'])
def start_scraper():
    print(f'Request: ${request.json}')
    url = request.json.get('url')
    search_text = request.json.get('search_text')

    # Run scraper asynchronously in a separate Python process
    # (invokes the main function with input arguments)
    command = f"python ./scraper/__init__.py {url} \"{search_text}\" /results"
    subprocess.Popen(command, shell=True)

    response = {'message': 'Scraper started successfully'}
    return jsonify(response), 200


# @app.route('/add-tracked-product', methods=['POST'])
# def add_tracked_product():
#     name = request.json.get('name')
#     tracked_product = TrackedProducts(name=name)
#     db.session.add(tracked_product)
#     db.session.commit()

#     response = {'message': 'Tracked product added successfully',
#                 'id': tracked_product.id}
#     return jsonify(response), 200


# @app.route('/tracked-product/<int:product_id>', methods=['PUT'])
# def toggle_tracked_product(product_id):
#     tracked_product = TrackedProducts.query.get(product_id)
#     if tracked_product is None:
#         response = {'message': 'Tracked product not found'}
#         return jsonify(response), 404

#     tracked_product.tracked = not tracked_product.tracked
#     db.session.commit()

#     response = {'message': 'Tracked product toggled successfully'}
#     return jsonify(response), 200


# @app.route('/tracked-products', methods=['GET'])
# def get_tracked_products():
#     tracked_products = TrackedProducts.query.all()

#     results = []
#     for product in tracked_products:
#         results.append({
#             'id': product.id,
#             'name': product.name,
#             'created_at': product.created_at,
#             'tracked': product.tracked
#         })

#     return jsonify(results), 200


# @app.route("/update-tracked-products", methods=["POST"])
# def update_tracked_products():
#     tracked_products = TrackedProducts.query.all()
#     url = "https://www.farmaciasoccavo.it/"

#     product_names = []
#     for tracked_product in tracked_products:
#         name = tracked_product.name
#         if not tracked_product.tracked:
#             continue

#         command = f"python ./scraper/__init__.py {url} \"{name}\" /results"
#         subprocess.Popen(command, shell=True)
#         product_names.append(name)

#     response = {'message': 'Scrapers started successfully',
#                 "products": product_names}
#     return jsonify(response), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
    # 0.0.0.0 allows for external call to be made on localhost, 0.0.0.0 or 127.0.0.1
