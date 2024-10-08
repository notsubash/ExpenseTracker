from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class invoice_summary(BaseModel):
    date: str = Field(default=None, description="The date of the invoice")
    category: str = Field(default=None, description="")
    description: str = Field(default=None, description="A brief description of the payment")
    amount: str = Field(default=None, description="The total amount paid")
    vat: str = Field(default=None, description="The total VAT (taxes) paid")
    business_personal: str = Field(default=None, description="Indicate whether the payment is for business or personal use")
    payment_method: str = Field(default=None, description="Indicate the method of payment used")

def get_category_list(state):
    categories_dict = state.get("categories_dict", {})
    return list(categories_dict.values())

def get_payment_method_list(state):
    payment_method_dict = state.get("payment_method_dict", {})
    return list(payment_method_dict.values())

def correct_node(state):
    date = state.get("date", "").strip()
    category = state.get("category", "").strip()
    description = state.get("description", "").strip()
    amount = state.get("amount", "").strip()
    vat = state.get("vat", "").strip()
    business_personal = state.get("business_personal", "").strip()
    payment_method = state.get("payment_method", "").strip()

    print(f"Date: {date}")
    print(f"Category: {category}")
    print(f"Description: {description}")
    print(f"Amount: {amount}")
    print(f"VAT: {vat}")
    print(f"Business/Personal: {business_personal}")
    print(f"Payment Method: {payment_method}")

    instructions = input("Let the LLM know what it has to change in the above summary of the invoice.")

    category_list = get_category_list(state)
    payment_method_list = get_payment_method_list(state)

    prompt = (
        f"Here's the summary of an invoice: \n"
        f"Date: {date}\n"
        f"Category: {category}\n"
        f"Description: {description}\n"
        f"Amount: {amount}\n"
        f"VAT: {vat}\n"
        f"Business/Personal: {business_personal}\n"
        f"Payment Method: {payment_method}\n"
        f"improve this summary based on the following user feedback:\n"
        f"Userfeedback: {instructions}\n"
        f"if the user asks to modify the category, make sure to choose one of the following categories:\n"
        f"{', '.join(category_list)}"
        f"if the user asks to modify the payment method, make sure to choose one of the following payment methods:\n"
        f"{', '.join(payment_method_list)}"
    )

    chat = ChatOpenAI(model='gpt-4o-mini', temperature=0)

    structured_llm = chat.with_structured_output(invoice_summary)

    messages = [HumanMessage(content=[{"type": "text", "text": prompt}])]

    response = structured_llm.invoke(messages)

    updated_date = response.dict().get("date", None)
    updated_category = response.dict().get("category", None)
    updated_description = response.dict().get("description", None)
    updated_amount = response.dict().get("amount", None)
    updated_vat = response.dict().get("vat", None)
    updated_business_personal = response.dict().get("business_personal", None)
    updated_payment_method = response.dict().get("payment_method", None)

    new_state = state.copy()

    new_state["date"] = updated_date
    new_state["category"] = updated_category
    new_state["description"] = updated_description
    new_state["amount"] = updated_amount
    new_state["vat"] = updated_vat
    new_state["business_personal"] = updated_business_personal
    new_state["payment_method"] = updated_payment_method

    if 'category' in new_state and 'categories_dict' in new_state:
        category = new_state["category"]
        categories_dict = new_state["categories_dict"]
        for key, value in categories_dict.items():
            if value == category:
                new_state["category_id"] = key
                break

    if 'payment_method' in new_state and 'payment_methods_dict' in new_state:
        payment_method = new_state["payment_method"]
        payment_methods_dict = new_state["payment_methods_dict"]
        for key, value in payment_methods_dict.items():
            if value == payment_method:
                new_state["payment_method_id"] = key
                break

    return new_state