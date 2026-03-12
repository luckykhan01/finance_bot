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

            await conn.execute(
                "UPDATE accounts SET balance = COALESCE(balance, 0) + $1 WHERE id = $2",
                balance_change,
                account_id
            )

            new_balance = await conn.fetchval(
                "SELECT balance FROM accounts WHERE id = $1",
                account_id
            )

            return new_balance

async def get_user_balances(user_id: int) -> list[dict]:
    """Return the balance of all accounts"""
    async with db.pool.acquire() as conn:
        records = await conn.fetch(queries.GET_ALL_BALANCES, user_id)
        return [dict(r) for r in records]


async def get_user_stats(user_id: int, t_type: str = "expense") -> list[dict]:
    """Return the statistics of one month"""
    async with db.pool.acquire() as conn:
        records = await conn.fetch(queries.GET_MONTHLY_STATS, user_id, t_type)
        return [dict(r) for r in records]
