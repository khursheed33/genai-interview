# Exercise 03 — Money Must Not Vanish (atomic transfer)

**Story:** Crash between debit and credit = money printed/vanished. Wrap it.

## Task
In `solution.py`, `transfer(conn, a, b, amt)` (autocommit connection given): `BEGIN IMMEDIATE`, balance check (raise `ValueError` if short), two updates, `COMMIT`; any error → `ROLLBACK` + re-raise.

## Acceptance
- Success moves exact amounts; overdraft raises and leaves BOTH balances untouched
- Balances helper `balances(conn)` provided for asserts
