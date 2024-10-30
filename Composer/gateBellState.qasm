// Bell State

OPENQASM 2.0;

include "qelib1.inc";
gate gateBellState a, b {
  h a;
  cx a, b;
}

qreg q[4];
creg c[4];