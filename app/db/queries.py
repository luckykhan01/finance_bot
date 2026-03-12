ENSURE_USER = """
    INSERT INTO users (id, username, full_name)
    VALUES ($1, $2, $3)
    ON CONFLICT (id) DO NOTHING;    
"""

GET_ACCOUNT = """
    SELECT id, balance FROM accounts WHERE user_id = $1 AND name = $2;
"""

CREATE_ACCOUNT = """
    INSERT INTO accounts (user_id, name, currency)
    VALUES ($1, $2, $3) RETURNING id, balance;
"""

ADD_TRANSACTION = """
    INSERT INTO transactions (account_id, amount, type, category, description)
    VALUES ($1, $2, $3, $4, $5)
"""

UPDATE_ACCOUNT_BALANCE = """
    UPDATE accounts SET balance = COALESCE(balance, 0) + $1 WHERE id = $2 RETURNING balance;
"""

GET_ALL_BALANCES = """
    SELECT name, balance, currency
    FROM accounts
    WHERE user_id = $1
    ORDER BY balance DESC;
"""

GET_MONTHLY_STATS = """
    SELECT category, SUM(amount) as total
    FROM transactions 
    WHERE account_id IN (SELECT id FROM accounts WHERE user_id = $1)
        AND type = $2
        AND date_trunc('month', created_at) = date_trunc('month', CURRENT_DATE)
    GROUP BY category
    ORDER BY total DESC; 
"""

