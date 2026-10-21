# Regulator Math

Adjustable linear regulator arithmetic. A 240 Ω and 1680 Ω pair around the 1.25 V reference sets the output to 10 V.

## What it computes

- **The divider truth** - the output voltage from the upper and lower divider resistors (0.01 to 1000000 Ω each): the 1.25 V reference times one plus the ratio.
- **The resistor truth** - the lower resistor for a target output (above the 1.25 V reference, up to 100 V), given the upper resistor.
- **The dissipation truth** - the heat from the drop times the current (0.01 to 10000000 mA).

The 1.25 V figure is a named chart constant from the classic adjustable three-terminal regulator datasheet.

## Boundary

Arithmetic only, with the reference treated as exactly 1.25 V and the adjust-pin current ignored. It has not seen any regulator and does not know the tolerance, the dropout behavior, the thermal limits or the part variant, and it gives no verdict that a regulator circuit is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers, half-up on display).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/regulatormath/
Repo: https://github.com/iLanis-agent/regulatormath
