#!/usr/bin/env python
# coding: utf-8

from environs import Env
from matplotlib import pyplot as plt

# import Qiskit libraries
from qiskit import QuantumCircuit
# from qiskit.providers.basic_provider import BasicProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2

from draperQFTAdder4Q import circuit as draperQFTAdderCircuit
from job import Job

# Read the IBM API token from the the .env file

env = Env()

#env.read_env()                         # this does not work (?)
env.read_env('.env', recurse=False)     # read .env file, if it exists

token = env('IBM_QUANTUM_TOKEN')  

print('>>>> Token: ' + token[:5] + '...')     # Check that the starting characters of the token are printed

# runs the circuit either on simulator or the IBM Quantym Platform
def run(job) :

    circuit = draperQFTAdderCircuit()

    if job.backend == "simulator":
        ibm_backend = FakeAlmadenV2()      
        backend_name = ibm_backend.name
    else: 
        service = QiskitRuntimeService(channel="ibm_quantum", token=token)

        if job.backend == "least_busy_QPU":
            ibm_backend = service.least_busy(simulator=False, operational=True)
        else:
            ibm_backend = service.backend(name=job.backend)
        
        backend_name = ibm_backend.name

    pm = generate_preset_pass_manager(backend=ibm_backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    if job.backend != "simulator" :
        ibm_backend = Sampler(mode=ibm_backend)

    ibm_job = ibm_backend.run([isa_circuit], shots=job.shots)
    print(f'>>>> Job ID: {ibm_job.job_id()} ({ibm_job.status()}) on {backend_name}, {job.shots} shots)')

    if job.backend == "simulator" :
        job.counts = ibm_job.result().get_counts()
    else:
        job.counts = {}

    # print(job.counts)

    job.job_id = ibm_job.job_id()
    job.backend = backend_name
    job.status = str(ibm_job.status())

    return job

# gets the results from a job hardware run
def results(job_id) :
    
    service = QiskitRuntimeService(channel="ibm_quantum", token=token)
    ibm_job = service.job(job_id)

    response = Job()
    response.job_id = job_id
    response.backend = ibm_job.backend().name
    response.status = str(ibm_job.status())

    if response.status == "DONE" :
        results = ibm_job.result()[0].data.c
        response.shots = results.num_shots
        response.counts = results.get_counts()
    else: # Job still pending
        response.shots = 0
        response.counts = {}

    return response
  
# plots the results of a job
def plot(job) : 

    plt.rcParams["figure.figsize"] = (20,8)
    plt.bar(job.counts.keys(), job.counts.values())
    plt.xlabel('States')
    plt.ylabel('Values')

    plt.show()

    return job

