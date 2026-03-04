from fastapi import APIRouter, HTTPException
from app.api.schemas import TransactionCreate
from app.services.finance import process_transaction

router = APIRouter()

@router.post("/transactions/")
async def add_transaction(tx: TransactionCreate):
    try:
        new_balance = await process_transaction(
            user_id=tx.user_id,
            username=tx.username,
            account_name=tx.account_name,
            amount=tx.amount,
            t_type=tx.t_type,
            category=tx.category,
            description=tx.description
        )

        return {
            "status": "success",
            "message": "Transaction completed successfully.",
            "account": tx.account_name,
            "new_balance": new_balance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))