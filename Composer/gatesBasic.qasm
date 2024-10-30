OPENQASM 2.0;

include "qelib1.inc";

gate toffoli a, b, c {
  ch a, c;
  cz b, c;
  ch a, c;
}

gate cZ a, b {
  cx a, b;
  cx b, a;
  cx a, b;
}

gate ccZ a, b, c {
  h c;
  ccx a, b, c;
  h c;
}

qreg q[4];
creg c[4];

