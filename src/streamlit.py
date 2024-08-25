import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import streamlit as st
import datetime
from decimal import Decimal, InvalidOperation
from api.expenses_routes import create_expense, ExpenseCreate, get_expenses, delete_expense
from api.category_routes import create_category, CategoryCreate, get_categories, delete_category
from api.payment_methods_routes import create_payment_method, PaymentMethodCreate, get_payment_methods, delete_payment_method
from chain.graphstate import setup_builder, create_graph_state
from chain.nodes.imageencoder import encode_image


def main():
    st.sidebar.title("Expense Tracker")
    pages = {
        "Process Receipt": process_receipt_page,
        "Expenses": expenses_page,
        "Categories": categories_page,
        "Payment Methods": payment_methods_page
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page()


def percentage_to_decimal(value):
    if isinstance(value, str):
        value = value.strip().replace('$', '').replace(',', '')
        if value.endswith('%'):
            return Decimal(value.rstrip('%')) / 100
    return Decimal(value) if value else Decimal('0')


def process_receipt_page():
    st.title("Process Receipt")

    if 'success_message' in st.session_state:
        st.success(st.session_state.success_message)
        del st.session_state.success_message
    
    uploaded_file = st.file_uploader("Choose a receipt image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Receipt", use_column_width=True)
        
        if st.button("Process Receipt"):
            with st.spinner("Processing receipt..."):
                image_base64 = encode_image(uploaded_file)
                initial_state = create_graph_state()
                initial_state["image_base64"] = image_base64
                
                builder = setup_builder()
                app = builder.compile()
                result = app.invoke(initial_state)
                st.success("Receipt processed successfully!")
                st.session_state.processed_result = result

        if 'processed_result' in st.session_state:
            result = st.session_state.processed_result
            st.subheader("Processed Information:")
            st.write(f"Date: {result.get('date')}")
            st.write(f"Description: {result.get('description')}")
            st.write(f"Amount: {result.get('amount')}")
            st.write(f"VAT: {result.get('vat')}")
            st.write(f"Business/Personal: {result.get('business_personal')}")
            st.write(f"Payment Method: {result.get('payment_method')}")
            st.write(f"Category: {result.get('category')}")
            
        # if st.button("Create Expense"):
        #                 vat_decimal = percentage_to_decimal(result['vat'])
        #                 expense = ExpenseCreate(
        #                     date=result['date'],
        #                     category_id=result['category_id'],
        #                     description=result['description'],
        #                     amount=Decimal(str(result['amount'])),
        #                     vat=vat_decimal,
        #                     payment_method_id=result['payment_method_id'],
        #                     business_personal=result['business_personal']
        #                 )
        #                 try:
        #                     created_expense = create_expense(expense)
        #                     if created_expense and 'transaction_id' in created_expense:
        #                         st.write(f"Expense created successfully! Transaction ID: {created_expense['transaction_id']}")
        #                         del st.session_state.processed_result
        #                         st.rerun()
        #                     else:
        #                         st.error("Failed to create expense. Please check the logs for more information.")
        #                         st.write("API Response:", created_expense)
        #                 except Exception as e:
        #                     st.error(f"An error occurred: {str(e)}")           


def expenses_page():
    st.title("Expenses")
    tab1, tab2 = st.tabs(["View Expenses", "Add Expense"])
    
    with tab1:
        view_expenses()
    
    with tab2:
        add_expense_form()

def categories_page():
    st.title("Categories")
    tab1, tab2 = st.tabs(["View Categories", "Add Category"])
    
    with tab1:
        view_categories()
    
    with tab2:
        add_category_form()

def payment_methods_page():
    st.title("Payment Methods")
    tab1, tab2 = st.tabs(["View Payment Methods", "Add Payment Method"])
    
    with tab1:
        view_payment_methods()
    
    with tab2:
        add_payment_method_form()

def view_expenses():
    expenses = get_expenses()
    for expense in expenses:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"{expense['date']} - {expense['description']} (${expense['amount']})")
        with col2:
            if st.button(f"Delete {expense['transaction_id']}", key=f"del_exp_{expense['transaction_id']}"):
                delete_expense(expense['transaction_id'])
                st.rerun()

def view_categories():
    categories = get_categories()
    for category in categories:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{category['category_name']}")
        with col2:
            if st.button(f"Delete {category['category_id']}", key=f"del_cat_{category['category_id']}"):
                delete_category(category['category_id'])
                st.rerun()

def view_payment_methods():
    payment_methods = get_payment_methods()
    for method in payment_methods:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{method['payment_method_name']}")
        with col2:
            if st.button(f"Delete {method['payment_method_id']}", key=f"del_pm_{method['payment_method_id']}"):
                delete_payment_method(method['payment_method_id'])
                st.rerun()

def add_expense_form():
    date = st.date_input("Date", datetime.date.today())
    category_id = st.number_input("Category ID", min_value=1, step=1)
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    vat = st.number_input("VAT", min_value=0.0, step=0.01)
    payment_method_id = st.number_input("Payment Method ID", min_value=1, step=1)
    business_personal = st.selectbox("Type", ["Business", "Personal"])

    if st.button("Add Expense"):
        expense = ExpenseCreate(
            date=date,
            category_id=category_id,
            description=description,
            amount=Decimal(str(amount)),
            vat=Decimal(str(vat)),
            payment_method_id=payment_method_id,
            business_personal=business_personal
        )
        result = create_expense(expense)
        st.success(f"Expense added successfully! Transaction ID: {result['transaction_id']}")

def add_category_form():
    category_name = st.text_input("Category Name")
    if st.button("Add Category"):
        category = CategoryCreate(category_name=category_name)
        result = create_category(category)
        st.success(f"Category added successfully! Category ID: {result['category_id']}")

def add_payment_method_form():
    payment_method_name = st.text_input("Payment Method Name")
    if st.button("Add Payment Method"):
        payment_method = PaymentMethodCreate(payment_method_name=payment_method_name)
        result = create_payment_method(payment_method)
        st.success(f"Payment method added successfully! Payment Method ID: {result['payment_method_id']}")

if __name__ == "__main__":
    main()
