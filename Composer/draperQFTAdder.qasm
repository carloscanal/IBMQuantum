OPENQASM 2.0;

include "qelib1.inc";

gate qft3Q a, b, c {
  h c;
  cp(pi / 2) b, c;
  cp(pi / 4) a, c;
  h b;
  cp(pi / 2) a, b;
  h a;
  swap a, c;
}

gate inv_qft3Q a, b, c {
  swap a, c;
  h a;
  cp(-pi / 2) b, a;
  cp(-pi / 4) c, a;
  h b;
  cp(-pi / 2) c, b;
  h c;
}

gate qft4Q a, b, c, d {
  h d;
  cp(pi / 2) c, d;
  cp(pi / 4) b, d;
  cp(pi / 8) a, d;
  h c;
  cp(pi / 2) b, c;
  cp(pi / 4) a, c;
  h b;
  cp(pi / 2) a, b;
  h a;
  swap b, c;
  swap a, d;
}

gate inv_qft4Q a, b, c, d {
  swap a, d;
  swap b, c;
  h a;
  cp(-pi / 2) b, a;
  cp(-pi / 4) c, a;
  cp(-pi / 8) d, a;
  h b;
  cp(-pi / 2) c, b;
  cp(-pi / 4) d, b;
  h c;
  cp(-pi / 2) d, c;
  h d;
}

gate adder3Q a, b, c {
  ccx a, b, c;
  cx a, b;
  x a;
}

gate adder4Q a, b, c, d {
  c3x a, b, c, d;
  ccx a, b, c;
  cx a, b;
  x a;
}

gate drapperAdder4Q a, b, c, d {
  qft4Q a, b, c, d;
  barrier a, b, c, d;
  t b;
  z d;
  p(pi/8) a;
  s c;
  barrier a, b, c, d;
  inv_qft4Q a, b, c, d;
}

qreg a[4];
creg c0[4];

drapperAdder a[0], a[1], a[2], a[3];
