from app.core.database import db
from app.db import queries


async def process_transaction(
    user_id: int,
    username: str,
    account_name: str,
    amount: float,
    t_type: str,
    category: str,
    description: str = ""
) -> float:
    """
    Writes new transaction and updates balance.
    Returns new balance.
    """
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(queries.ENSURE_USER, user_id, username, username)

            account = await conn.fetchrow(queries.GET_ACCOUNT, user_id, account_name)

            if not account:
                account = await conn.fetchrow(queries.CREATE_ACCOUNT, user_id, account_name, 'KZT')

            account_id = account['id']

            await conn.execute(
                queries.ADD_TRANSACTION,
                account_id, amount, t_type, category, description
            )

            balance_change = amount if t_type == 'income' else -amount

            new_balance = await conn.fetchval(
                queries.UPDATE_ACCOUNT_BALANCE,
                balance_change, user_id
            )

            return new_balance