OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
x q[0];
barrier q[0], q[1], q[2], q[3];
c3x q[0], q[1], q[2], q[3];
ccx q[0], q[1], q[2];
cx q[0], q[1];
x q[0];