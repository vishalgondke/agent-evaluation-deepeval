from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s "
)

@tool
def get_user_purchase_history(user_id: str) -> dict:
    """
    Get the purchase history of a user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        dict[str, PurchaseItem]: A dictionary mapping item names to PurchaseItem objects representing the user's purchase history.
    """
    logging.info(f"Using get_user_purchase_history tool to fetch purchase history for user_id: {user_id}")
    if users_data.get(user_id):
        return users_data[user_id]
    return {"status": f"No purchase history found for user_id: {user_id}"}

@tool
def calculate_right_refund(user_id: str, items: list[PurchaseItem]) -> str:
    """
    Calculate the right refund amount for a user based on their purchase history and the items they want to refund.

    Args:
        user_id (str): The ID of the user.
        items (list[PurchaseItem]): A list of PurchaseItem objects representing the items the user wants to refund.

    Returns:
        str: A message indicating the total refund amount or an error message if the user or items are not found.
    """
    logging.info(f"Using calculate_right_refund tool to calculate refund for user_id: {user_id} and items: {items}")
    if users_data.get(user_id):
        total_refund = 0
        for item in items:
            if item.name in users_data[user_id]:
                total_refund += users_data[user_id][item.name]["price"] * item.quantity
            else:
                return f"Item '{item.name}' not found in purchase history for user_id: {user_id}"
        return f"Total refund amount for user_id {user_id} is: ${total_refund}"
    return f"No purchase history found for user_id: {user_id}"

@tool
def issue_refund_ticket(user_id: str, items: list[PurchaseItem], refund_amount: float) -> str:
    """
    Issue a refund ticket for a user.

    Args:
        user_id (str): The ID of the user.
        items (list[PurchaseItem]): A list of PurchaseItem objects representing the items being refunded.
        refund_amount (float): The total refund amount.

    Returns:
        str: A message indicating that the refund ticket has been issued or an error message if the user is not found.
    """
    logging.info(f"Using issue_refund_ticket tool to issue refund ticket for user_id: {user_id}, items: {items}, refund_amount: {refund_amount}")
    if users_data.get(user_id):
        # Here you would typically create a refund ticket in your system
        return f"Refund ticket issued for user_id {user_id} with amount ${refund_amount} for items: {[item.name for item in items]}"
    return f"No purchase history found for user_id: {user_id}"

@tool
def check_current_date() -> str:
    """
    Check the current date.
    Only needs to be called when the agent needs to check if the purchase date is within 30 days for a refund.
    If it is more than 30 days, then the agent should not proceed with the refund.

    Returns:
        str: The current date in YYYY-MM-DD format.
    """
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    logging.info(f"Using check_current_date tool to get current date: {current_date}")
    return current_date


# print(get_user_purchase_history.invoke("user123"))
# book = PurchaseItem(name="book",price=23,quantity=1)
# pen = PurchaseItem(name="pen",price=7,quantity=5)
# print(calculate_right_refund.invoke({"user_id":"user123","items":[book,pen]}))
# print("--------------------")
# print(issue_refund_ticket.invoke({"user_id":"user123","items":[book,pen],"refund_amount":58}))
# print(check_current_date.invoke({"user_id":"user123"}))