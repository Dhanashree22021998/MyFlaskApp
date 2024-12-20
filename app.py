from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from security import *
import requests
from flasgger import Swagger

app = Flask(__name__)

swagger = Swagger(app)

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key
jwt = JWTManager(app)

users = {"testuser": "password123"}



# Function to fetch all coins (with CoinGecko IDs)
def get_all_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    return response.json()

# 1) API to list all coins with their CoinGecko ID
@app.route('/api/coins', methods=['GET'])
def list_all_coins():

    """
    Fetch a list of all available coins with their CoinGecko ID
    ---
    responses:
      200:
        description: A list of coins with their CoinGecko ID
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: 'bitcoin'
              name:
                type: string
                example: 'Bitcoin'
              symbol:
                type: string
                example: 'BTC'
      500:
        description: Internal server error
    """
    try:
        coins = get_all_coins()
        return jsonify(coins), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to fetch all coin categories
def get_coin_categories():
    url = "https://api.coingecko.com/api/v3/coins/categories/list"
    response = requests.get(url)
    return response.json()

# 2) API to list all coin categories
@app.route('/api/coin-categories', methods=['GET'])
def list_coin_categories():
    try:
        categories = get_coin_categories()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to fetch coins based on certain criteria
def get_coins_by_criteria(page=1, per_page=10, order="market_cap_desc"):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': order,
        'per_page': per_page,
        'page': page
    }
    response = requests.get(url, params=params)
    return response.json()

# 3) API to list coins according to criteria (e.g., based on market cap)
@app.route('/api/coins/markets', methods=['GET'])
def list_coins_by_criteria():
    try:
        # Get optional query parameters (page, per_page, and order)
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        order = request.args.get('order', default="market_cap_desc", type=str)

        coins = get_coins_by_criteria(page, per_page, order)
        return jsonify(coins), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    print('Login Called------->')
    # Get username and password from the request
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Check if the username exists and the password is correct
    if username in users and users[username] == password:
        # Create JWT token (access token)
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Get the identity (user) from the JWT
    current_user = get_jwt_identity()

    return jsonify(message=f"Hello, {current_user}! This is a protected route.")



# Run the app
if __name__ == '__main__':
    app.run(debug=True)