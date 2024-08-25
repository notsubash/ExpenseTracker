import streamlit as st

def humancheck_node(state):
    image_location = state.get("image_location")
    image_location = image_location.strip() if image_location else None
    
    category = state.get("category")
    category = category.strip() if isinstance(category, str) else category
    
    payment_method = state.get("payment_method")
    payment_method = payment_method.strip() if isinstance(payment_method, str) else payment_method
    
    amount = state.get("amount")
    amount = str(amount).strip() if amount is not None else None
    
    date = state.get("date")
    date = date.strip() if isinstance(date, str) else date
    
    description = state.get("description")
    description = description.strip() if isinstance(description, str) else description
    
    vat = state.get("vat")
    vat = str(vat).strip() if vat is not None else None
    
    business_personal = state.get("business_personal")
    business_personal = business_personal.strip() if isinstance(business_personal, str) else business_personal

    # Convert amount to float if it's not None
    if amount is not None:
        try:
            amount = float(amount)
        except ValueError:
            amount = None
    
    # Convert vat to float if it's not None
    if vat is not None:
        try:
            vat = float(vat)
        except ValueError:
            vat = None

    new_state = state.copy()

    st.write(f"Image Location: {image_location}")
    st.write(f"Date: {date}")
    st.write(f"Category: {category}")
    st.write(f"Description: {description}")
    st.write(f"Amount: {amount}")
    st.write(f"VAT: {vat}")
    st.write(f"Business/Personal: {business_personal}")
    st.write(f"Payment Method: {payment_method}")

    new_state["user_decision_needed"] = True

    return new_state



