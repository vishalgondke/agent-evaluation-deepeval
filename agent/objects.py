from pydantic import BaseModel, Field

class Answer(BaseModel):
    conversation_id: str = Field(description="The ID of the conversation.")
    answer: str = Field(description="The content of the answer.")
    conversation: bool = Field(description="Indicates if the converstaion should still continue or no." \
        "If the agent jas already made the decision about refund should not be proceeded, then this should be set to False" \
        "If the agent has not made the decision about refund or needs more talk, then this should be set to True",default=True)

class PurchaseItem(BaseModel):
    name: str = Field(description="The name of the item purchased.")
    price: int = Field(description="The price of the item purchased.")
    quantity: int = Field(description="The quantity of the item purchased.")