# Exercise 04 — Undo Legs (orchestrated saga + reverse compensation)

**Story:** Payment succeeded, stock failed, shipment never ran. Customer got charged for nothing. Choreograph the undo.

## Task
In `solution.py`, `run(order, fail_at=None)` over steps pay→stock→ship (each `(name, do_ok, compensate)`): run in order; on first failure (or `fail_at` name) run compensations for COMPLETED steps in REVERSE; return `("done", [])` or `("failed:<step>", [compensated names in run order])`.

## Acceptance
- Happy path done; `fail_at="stock"` → failed + compensated `["pay"]`; `fail_at="ship"` → compensated `["stock", "pay"]` (reverse!)
