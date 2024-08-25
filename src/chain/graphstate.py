from chain.nodes.imageencoder import image_encoder_node
from chain.nodes.jsonparser import json_parsing_node
from chain.nodes.categorizer import categorizer_node
from chain.nodes.humancheck import humancheck_node
from chain.nodes.db_entry import db_entry_node
from chain.nodes.correct import correct_node

from chain.helpers.get_payment_methods_and_categories import get_payment_methods, get_categories

from typing import TypedDict, Optional, Dict
from datetime import date
from decimal import Decimal
from langgraph.graph import StateGraph, END
from langsmith import Client
import os
from uuid import uuid4
from dotenv import load_dotenv
import uvicorn

load_dotenv()

unique_id = uuid4().hex[:8]
os.environ["LANGCHAIN_PROJECT"] = "ExpenseTracker"
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

client = Client(api_key=langsmith_api_key)

class GraphState(TypedDict):
    user_decision: Optional[list]
    image_base64: Optional[str]
    image_location: Optional[str]
    date: Optional[date]
    category_id: Optional[int]
    description: Optional[str]
    amount: Optional[Decimal]
    vat: Optional[Decimal]
    payment_method_id: Optional[int]
    business_personal: Optional[str]
    category: Optional[str]
    payment_method: Optional[str]
    payment_methods_dict: Optional[Dict[int, str]]
    categories_dict: Optional[Dict[int, str]]

def create_graph_state() -> GraphState:
    payment_methods_dict = get_payment_methods()
    categories_dict = get_categories()

    return {
        "user_decision": None,
        "image_base64": None,
        "image_location": None,
        "date": None,
        "category_id": None,
        "description": None,
        "amount":None,
        "vat": None,
        "payment_method_id": None,
        "business_personal": None,
        "category": None,
        "payment_method": None,
        "payment_methods_dict": payment_methods_dict,
        "categories_dict": categories_dict
    }

def setup_builder() -> StateGraph:
    builder = StateGraph(GraphState)

    builder.add_node("image_encoder", image_encoder_node)
    builder.add_node("json_parser", json_parsing_node)
    builder.add_node("categorizer", categorizer_node)
    builder.add_node("db_entry", db_entry_node)
    #builder.add_node("humancheck", humancheck_node)

    builder.add_edge("image_encoder", "json_parser")
    builder.add_edge("json_parser", "categorizer")
    #builder.add_edge("categorizer", "humancheck")
    builder.add_edge("categorizer", "db_entry")

    
    #builder.add_node("correct", correct_node)

    # def decide_humancheck(state):
    #     if state.get('user_decision') == "accept":
    #         return "db_entry"
    #     elif state.get('user_decision') == "change_model":
    #         return "json_parser"
    #     elif state.get('user_decision') == "correct":
    #         return "correct"
    #     return None
    
    # builder.add_conditional_edges("humancheck", decide_humancheck, {
    #     "db_entry": "db_entry",
    #     "json_parser": "json_parser",
    #     "correct": "correct",
    # })

    # builder.add_edge("correct", "humancheck")

    builder.set_entry_point("image_encoder")
    builder.add_edge("db_entry", END)

    return builder

def main():
    builder = setup_builder()
    app = builder.compile()

    initial_state = create_graph_state()

    initial_state["image_location"] = "/Users/subash/Documents/ExpenseTracker/data/walmart-bon.jpeg"

    result = app.invoke(initial_state)

    print("Final state after processing:", result)

    if "transaction_id" in result:
        print(f"Expense successfully added with transaction ID: {result['transaction_id']}")
    else:
        print("Expense was not added. Check the final state for errors.")

if __name__ == "__main__":
    main()