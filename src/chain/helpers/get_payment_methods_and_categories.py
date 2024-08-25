import requests
import time
import logging

def get_payment_methods(max_retries=3, retry_delay=1) -> str:
    url = "http://localhost:8000/payment_methods"
    fallback_methods = {1: 'Credit Card', 2: 'Debit Card', 3: 'Cash', 4: 'Bank Transfer'}
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return {method['payment_method_id']: method['payment_method_name'] for method in response.json()}
        except requests.RequestException as e:
            logging.error(f"Error fetching payment methods: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    
    logging.warning("Failed to fetch payment methods. Using fallback methods.")
    return fallback_methods
    
def get_categories() -> dict:
    url = 'http://localhost:8000/categories'
    response = requests.get(url, headers={"accept": "application/json"})

    if response.status_code == 200:
        categories = response.json()
        categories_dict = {
            item["category_id"]: item["category_name"]
            for item in categories
        }
        return categories_dict
    else:
        raise  Exception("Failed to fetch categories. Status code: {}".format(response.status_code))