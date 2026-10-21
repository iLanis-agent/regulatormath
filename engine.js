// Regulator Math engine: output voltage from the divider pair around the 1.25 V reference, the lower resistor for a target output, and the dissipation from the drop times the current. Exact integers (hundredths of a V, hundredths of an Ω, hundredths of a mA, hundredths of a mW), half-up on display only. The 1.25 V reference is a named chart constant from the classic adjustable three-terminal regulator datasheet.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _R = "each resistor must be from 0.01 to 1000000 Ω with at most two decimal places";
var _V = "each voltage must be from 0.01 to 100 V with at most two decimal places";
var _I = "the current must be from 0.01 to 10000000 mA with at most two decimal places";
var _REF = "the output must be above the 1.25 V reference";
var _DROP = "the input must be more than the output so the regulator sees a drop";
var VREF = 125;
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  if (v < 0) return "-" + _dec(-v, places);
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _res(t) { return _p(t, _R, 7, 2, 1, 100000000); }
function _volt(t) { return _p(t, _V, 3, 2, 1, 10000); }

function dividerTruth(r1, r2) {
  var a = _res(r1), b = _res(r2);
  var v = _hu(VREF * (a + b), a);
  return "A " + _dec(a, 2) + " Ω upper and " + _dec(b, 2) + " Ω lower resistor around the 1.25 V reference sets the output to " + _dec(v, 2) + " V.";
}
function resistorTruth(vout, r1) {
  var v = _volt(vout), a = _res(r1);
  if (v <= VREF) throw new Error(_REF);
  var b = _hu(a * (v - VREF), VREF);
  return "For a " + _dec(v, 2) + " V output with a " + _dec(a, 2) + " Ω upper resistor, the lower resistor comes to " + _dec(b, 2) + " Ω.";
}
function dissipTruth(vin, vout, iout) {
  var vi = _volt(vin), vo = _volt(vout), i = _p(iout, _I, 8, 2, 1, 1000000000);
  var d = vi - vo;
  if (d <= 0) throw new Error(_DROP);
  var p = _hu(d * i, 100);
  return "Dropping " + _dec(vi, 2) + " V to " + _dec(vo, 2) + " V at " + _dec(i, 2) + " mA leaves the regulator burning " + _dec(p, 2) + " mW.";
}
