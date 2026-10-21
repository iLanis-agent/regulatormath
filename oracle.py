import json, random
from fractions import Fraction

def hu(num, den):
    return Fraction((2*num + den) - ((2*num + den) % (2*den)), 2*den)

def dec(v, places=2):
    if v < 0: return "-" + dec(-v, places)
    base = 10**places
    n = v.numerator // v.denominator
    s = str(n // base); f = str(n % base).zfill(places).rstrip("0")
    return s + "." + f if f else s

def s100(n):
    w, f = divmod(n, 100)
    return f"{w}.{f:02d}".rstrip("0").rstrip(".")

VREF = 125

def divider(a, b):
    v = hu(VREF*(a+b), a)
    return (f"A {dec(Fraction(a))} Ω upper and {dec(Fraction(b))} Ω lower resistor around the 1.25 V reference "
            f"sets the output to {dec(v)} V.")
def resistor(v, a):
    assert v > VREF
    b = hu(a*(v-VREF), VREF)
    return (f"For a {dec(Fraction(v))} V output with a {dec(Fraction(a))} Ω upper resistor, "
            f"the lower resistor comes to {dec(b)} Ω.")
def dissip(vi, vo, i):
    d = vi - vo; assert d > 0
    p = hu(d*i, 100)
    return (f"Dropping {dec(Fraction(vi))} V to {dec(Fraction(vo))} V at {dec(Fraction(i))} mA "
            f"leaves the regulator burning {dec(p)} mW.")

random.seed(736)
cases = [
  dict(fn="divider", args=["240","1680"], expect=divider(24000,168000)),
  dict(fn="resistor", args=["10","240"], expect=resistor(1000,24000)),
  dict(fn="dissip", args=["15","10","500"], expect=dissip(1500,1000,50000)),
]
for _ in range(30):
    a = random.randint(1,100000000); b = random.randint(1,100000000)
    cases.append(dict(fn="divider", args=[s100(a),s100(b)], expect=divider(a,b)))
for _ in range(30):
    v = random.randint(126,10000); a = random.randint(1,100000000)
    cases.append(dict(fn="resistor", args=[s100(v),s100(a)], expect=resistor(v,a)))
for _ in range(30):
    vo = random.randint(1,9999); vi = random.randint(vo+1,10000); i = random.randint(1,1000000000)
    cases.append(dict(fn="dissip", args=[s100(vi),s100(vo),s100(i)], expect=dissip(vi,vo,i)))
errcases = [
  ("divider", ["0","1680"]), ("divider", ["240","1000000.01"]), ("divider", ["24.005","1680"]),
  ("resistor", ["1.25","240"]), ("resistor", ["1","240"]), ("resistor", ["10","0"]),
  ("resistor", ["0","240"]), ("resistor", ["100.01","240"]),
  ("dissip", ["10","10","500"]), ("dissip", ["9","10","500"]), ("dissip", ["15","10","0"]),
  ("dissip", ["15","10","10000000.01"]), ("dissip", ["0","10","500"]),
]
json.dump({"cases": cases, "errors": errcases}, open("expected.json","w"), ensure_ascii=False, indent=1)
open("expected.json","a").write("\n")
print("expected.json written:", len(cases), "cases")
