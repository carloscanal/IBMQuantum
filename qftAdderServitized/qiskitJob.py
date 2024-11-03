#!/usr/bin/env python
# coding: utf-8

from environs import Env

from matplotlib import pyplot as plt

# import circuit from from draperQFTAdder4Q.py
from draperQFTAdder4Q import circuit as draperQFTAdderCircuit

# import Qiskit libraries
from qiskit import QuantumCircuit
# from qiskit.providers.basic_provider import BasicProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2

# Read the IBM API token from the the .env file

env = Env()

#env.read_env()                         # this does not work (?)
env.read_env('.env', recurse=False)     # read .env file, if it exists

token = env('IBM_QUANTUM_TOKEN')  

print('>>>> Token: ' + token[:5] + '...')     # Check that the starting characters of the token are printed

# define the list of QPUs available

qpus = ["simulator", "least_busy_QPU", "ibm_brisbane", "ibm_sherbrooke", "ibm_kyiv"]


# run the circuit on IBM Quantym Platform
def run(machine, shots):
    circuit = draperQFTAdderCircuit()

    if machine == "simulator":
        backend = FakeAlmadenV2()      
        backend_name = backend.name
    else: 
        service = QiskitRuntimeService(channel="ibm_quantum", token=token)

        if machine == "least_busy_QPU":
            backend = service.least_busy(simulator=False, operational=True)
        else:
            backend = service.get_backend(machine)
        
        backend_name = backend.name

    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    if machine != "simulator" :
        backend = Sampler(mode=backend)

    job = backend.run([isa_circuit], shots=int(shots))
    print(f'>>>> Job ID: {job.job_id()} ({job.status()}) on {backend_name}, {shots} shots)')

    if machine == "simulator" :
        return results(job=job, job_id="last_simulation")
    else:  
        return job.job_id()

def results(job, job_id) :   # "last_simulation", or alternatively a job_id previously run on the platform

    if job_id == "last_simulation":
        result = job.result()
    else:
        service = QiskitRuntimeService(channel="ibm_quantum", token=token)
        job = service.job(job_id)
        result = job.result()[0].data.c

    counts = result.get_counts()
    print(counts)

    plt.rcParams["figure.figsize"] = (20,8)
    plt.bar(counts.keys(), counts.values())
    plt.xlabel('States')
    plt.ylabel('Values')

    plt.show()

    return counts
