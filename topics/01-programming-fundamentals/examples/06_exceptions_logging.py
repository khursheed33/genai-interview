"""06_exceptions_logging.py — fire alarm with room number, not shouting.

Run: uv run python topics/01-programming-fundamentals/examples/06_exceptions_logging.py
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("shop")


class PaymentFailed(Exception):
    pass


def charge(amount, balance):
    if amount > balance:
        raise PaymentFailed(f"need {amount}, have {balance}")
    return balance - amount


order_id = "ORD-101"
try:
    left = charge(500, 100)
except PaymentFailed:
    logger.exception("charge failed order_id=%s", order_id)  # logs traceback + context
    print("told user: payment failed, no money taken")
else:
    print("dispatch, balance left:", left)
finally:
    print("released seat lock (always)")

# custom exception lets caller catch exactly this, not all errors
print("OK — specific exceptions, logger with context, never log card numbers")
