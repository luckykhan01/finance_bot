from fastapi import APIRouter, HTTPException
from app.api.schemas import TransactionCreate, RawTransactionText
from app.services.finance import process_transaction
from app.core.ai_client import parse_transaction_text

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


@router.post("/transactions/parse")
async def parse_and_add_transaction(raw_data: RawTransactionText):
    ai_result = await parse_transaction_text(raw_data.text)

    if not ai_result:
        raise HTTPException(status_code=400, detail="The transaction text could not be recognized.")

    try:
        new_balance = await process_transaction(
            user_id=raw_data.user_id,
            username=raw_data.username,
            account_name=ai_result['account_name'],
            amount=ai_result["amount"],
            t_type=ai_result["t_type"],
            category=ai_result["category"],
            description=ai_result.get("description", raw_data.text)
        )

        return {
            "status": "success",
            "message": f"Transaction '{raw_data.text}' successfully processed and recorded.",
            "parsed_data": ai_result,
            "new_balance": new_balance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))