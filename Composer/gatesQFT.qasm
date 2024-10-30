OPENQASM 2.0;

include "qelib1.inc";

// QFT - 3 qubits

gate qft3Q a, b, c {
  h c;
  cp(pi / 2) b, c;
  cp(pi / 4) a, c;
  h b;
  cp(pi / 2) a, b;
  h a;
  swap a, c;
}

// inverse QFT - 3 qubits

gate inv_qft3Q a, b, c {
  swap a, c;
  h a;
  cp(-pi / 2) b, a;
  cp(-pi / 4) c, a;
  h b;
  cp(-pi / 2) c, b;
  h c;
}

// QFT - 4 qubits

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

// inverse QFT - 4 qubits

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


qreg q[4];
creg c[4];

