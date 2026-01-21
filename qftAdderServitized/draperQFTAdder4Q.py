from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

def draperQFTAdder4Q() :

  qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";

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

    gate draperQFTAdder4Q a, b, c, d {
      qft4Q a, b, c, d;
      barrier a, b, c, d;
      p(pi / 8) a;
      t b;
      s c;
      z d;
      barrier a, b, c, d;
      inv_qft4Q a, b, c, d;
    }

    qreg a[4];

    draperQFTAdder4Q a[0], a[1], a[2], a[3];
   
    """
  qftAdder4Q = QuantumCircuit.to_gate(QuantumCircuit.from_qasm_str(qasm))

  qftAdder4Q.name = 'QFTAdder4Q'

  return qftAdder4Q

def circuit() :

  qreg_q = QuantumRegister(4, 'q')
  creg_c = ClassicalRegister(4, 'c')
  circuit = QuantumCircuit(qreg_q, creg_c)

  # Input: qubits 0 and 1 in superposition
  circuit.h(qreg_q[0])
  circuit.h(qreg_q[1])

  # Alternative input: 0110 (6)
  # circuit.x(qreg_q[1])
  # circuit.x(qreg_q[2])

  circuit.append(draperQFTAdder4Q(), [qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3]])

  circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3])

  circuit.measure(qreg_q[0], creg_c[0])
  circuit.measure(qreg_q[1], creg_c[1])
  circuit.measure(qreg_q[2], creg_c[2])
  circuit.measure(qreg_q[3], creg_c[3])

  return circuit