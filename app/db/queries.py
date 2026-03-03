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
    UPDATE accounts SET balance = balance + $1 WHERE id = $2 RETURNING balance;
"""