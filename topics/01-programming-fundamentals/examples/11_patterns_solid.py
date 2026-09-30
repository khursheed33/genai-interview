"""11_patterns_solid.py — vending machine, thali builder, route strategies.

Run: uv run python topics/01-programming-fundamentals/examples/11_patterns_solid.py
"""

from __future__ import annotations


# Strategy: different routes to school (swap without editing checkout)
class UPIPay:
    def pay(self, amt):
        return f"upi {amt}"


class CardPay:
    def pay(self, amt):
        return f"card {amt}"


class Checkout:
    def __init__(self, strategy):  # Dependency Injection: tiffin delivered
        self.strategy = strategy

    def buy(self, amt):
        return self.strategy.pay(amt)


print(Checkout(UPIPay()).buy(100))  # upi 100
print(Checkout(CardPay()).buy(100))  # card 100


# Factory: vending machine for LLM clients
def make_llm(kind):
    return {"openai": "gpt-4o", "ollama": "llama3"}[kind]


print("llm:", make_llm("ollama"))


# Observer: class group broadcast
class Group:
    def __init__(self):
        self.fans = []

    def join(self, fn):
        self.fans.append(fn)

    def post(self, msg):
        for fn in self.fans:
            fn(msg)


g = Group()
g.join(lambda m: print("asha got:", m))
g.join(lambda m: print("bob got:", m))
g.post("dosa ready!")

# Singleton via module-level instance (simplest, testable if injected)
print("OK — Strategy+Factory+Observer+DI cover most GenAI service code")
