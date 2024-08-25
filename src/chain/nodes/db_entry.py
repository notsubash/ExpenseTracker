import requests

def db_entry_node(state):
    def get_str_safe(key):
        value = state.get(key, "")
        if isinstance(value, str):
            return value.strip()
        else:
            return str(value)
    
    date = get_str_safe("date")
    category_id = get_str_safe("category_id")
    description = get_str_safe("description")
    amount = get_str_safe("amount")
    vat = get_str_safe("vat")
    business_personal = get_str_safe("business_personal")
    payment_method_id = get_str_safe("payment_method_id")

    url = "http://localhost:8000/expenses"

    data = {
        "date": date,
        "category_id": category_id,
        "description": description,
        "amount": amount,
        "vat": vat,
        "business_personal": business_personal,
        "payment_method_id": payment_method_id
    }

    #Making the POST request to the endpoint
    try:
        response = requests.post(url, json=data)

        if response.status_code == 201:
            print("Expense created successfully!")
            transaction_id = response.json().get("transaction_id")
            state["transaction_id"] = transaction_id
        else: 
            print("Failed to create expense.")
            print("Status Code:", response.status_code)
            print(f"Response: ", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return state