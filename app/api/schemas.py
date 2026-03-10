from pydantic import BaseModel, Field

class TransactionCreate(BaseModel):
    user_id: int = Field(..., example=123456789)
    username: str = Field(..., example='johndoe')
    account_name: str = Field(..., example='Kaspi')
    amount: float = Field(..., gt=0, example=5000.0)
    t_type: str = Field(..., pattern="^(income|expense)$", example="expense")
    category: str = Field(..., example='Food')
    description: str = Field(default="", example="Eating outside")

class RawTransactionText(BaseModel):
    user_id: int = Field(..., example=123456789)
    username: str = Field(..., example='johndoe')
    text: str = Field(..., example='-5000 Kaspi food')


