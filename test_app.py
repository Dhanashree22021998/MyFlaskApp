import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        """Set up the test client"""
        self.app = app.test_client()
        self.app.testing = True

    # Test for /api/coins endpoint
    @patch('requests.get')
    def test_list_all_coins(self, mock_get):
        mock_response = [{'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC'}]
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        
        response = self.app.get('/api/coins')
        
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("id", data[0])
        self.assertIn("name", data[0])
        self.assertIn("symbol", data[0])

    # Test for /api/coin-categories endpoint
    @patch('requests.get')
    def test_list_coin_categories(self, mock_get):
        mock_response = [{'id': 'decentralized-finance-defi', 'name': 'Decentralized Finance (DeFi)'}]
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        
        response = self.app.get('/api/coin-categories')
        
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("id", data[0])
        self.assertIn("name", data[0])

    # Test for /api/coins/markets endpoint
    @patch('requests.get')
    def test_list_coins_by_criteria(self, mock_get):
        mock_response = [{
            'id': 'bitcoin',
            'symbol': 'BTC',
            'name': 'Bitcoin',
            'current_price': 30000.5,
            'market_cap': 600000000000,
            'total_volume': 5000000000
        }]
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        
        response = self.app.get('/api/coins/markets?page=1&per_page=10&order=market_cap_desc')
        
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("id", data[0])
        self.assertIn("name", data[0])
        self.assertIn("current_price", data[0])

    # # Test for /login endpoint (POST)
    def test_login_success(self):
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'password123'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("access_token", data)

    def test_login_failure(self):
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'wrongpassword'})
        
        self.assertEqual(response.status_code, 401)
        data = response.json
        self.assertIn("msg", data)

    # # Test for /protected endpoint (GET)
    # @patch('requests.get')
    # def test_protected(self, mock_get):
    #     # Mocking JWT-related function
    #     with self.app.session_transaction() as session:
    #         session['jwt_token'] = 'test_token'
        
    #     response = self.app.get('/protected', headers={'Authorization': 'Bearer test_token'})
        
    #     self.assertEqual(response.status_code, 200)
    #     data = response.json
    #     self.assertIn("message", data)

    # # Test for missing endpoint
    def test_missing_endpoint(self):
        response = self.app.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
    
    # # Test for invalid order query parameter
    @patch('requests.get')
    def test_invalid_order(self, mock_get):
        response = self.app.get('/api/coins/markets?order=invalid_order')
        self.assertEqual(response.status_code, 500)
        data = response.json
        self.assertIn("error", data)

    # # Test for pagination behavior (page 1 vs page 2)

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up the test client"""
        self.app = app.test_client()
        self.app.testing = True

    @patch('requests.get')
    def test_pagination(self, mock_get):
        # Mock responses for two pages
        mock_response_1 = [{
            'id': 'bitcoin',
            'symbol': 'BTC',
            'name': 'Bitcoin',
            'current_price': 30000.5,
            'market_cap': 600000000000,
            'total_volume': 5000000000
        }]
        mock_response_2 = [{
            'id': 'raydium',
            'symbol': 'ray',
            'name': 'Raydium',
            'current_price': 4.07,
            'market_cap': 1189774375,
            'total_volume': 165273897
        }]

        # Side effect function to mock different responses based on the page number
        def mock_side_effect(url='/api/coins/markets/', params=None):
            # Ensure the params are properly passed
            #print(f"Mock URL: {url}")  # This will print the URL being called
            #print(f"Mock Params: {params}")  # This will print the query params

            if params:
                if params.get('page') == 1:
                    return mock_response_1
                elif params.get('page') == 2:
                    return mock_response_2
            return []  # Default empty response if no matching page

        # Set the side effect function for the mock
        #mock_get.return_value.json.side_effect = mock_side_effect
        mock_get.side_effect = mock_side_effect
        mock_get.return_value.status_code = 200

        # First page request
        response1 = self.app.get('/api/coins/markets?page=1&per_page=1')
        #print(f"Response1 Status Code: {response1.status_code}")
        #print(f"Response1 Data: {response1.json}")

        # Second page request
        response2 = self.app.get('/api/coins/markets?page=2&per_page=1')
        #print(f"Response2 Status Code: {response2.status_code}")
        #print(f"Response2 Data: {response2.json}")

        # Ensure status code is 200 for both
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

        # Ensure the IDs are different for pagination
        self.assertNotEqual(response1.json[0]['id'], response2.json[0]['id'])

if __name__ == '__main__':
    unittest.main()









'''

    @patch('requests.get')
    def test_pagination(self, mock_get):
        mock_response_1 = [{
            'id': 'bitcoin',
            'symbol': 'BTC',
            'name': 'Bitcoin',
            'current_price': 30000.5,
            'market_cap': 600000000000,
            'total_volume': 5000000000
        }]

        mock_response_2 = [{
            'id': 'raydium',
            'symbol': 'ray',
            'name': 'Raydium',
            'current_price': 4.07,
            'market_cap': 1189774375,
            'total_volume': 165273897
        }]
        
        # Side effect function to return different data based on page number
        def mock_side_effect(url, params=None):
            print("Mock Url", url)
            print("Params", params)
            if params and params.get('page') == '1':
                return mock_response_1
            elif params and params.get('page') == '2':
                return mock_response_2
            return []
        mock_get.return_value.json.return_value = mock_side_effect
        mock_get.return_value.status_code = 200
        
        # First page request
        response1 = self.app.get('/api/coins/markets?page=1&per_page=10&order=market_cap_desc')
        response2 = self.app.get('/api/coins/markets?page=1&per_page=10')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        data1 = response1.json
        data2 = response2.json
        
        print('data1 --> ', data1)
        print('data2 --> ', data2)

        self.assertEqual(data1[0]['id'],data2[0]["id"])  # Ensure results differ


if __name__ == '__main__':
    unittest.main()
'''