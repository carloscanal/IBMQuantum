
# ejecutar con    python -m uvicorn main:api --reload --host 0.0.0.0 --port 8000

import jsonify

from fastapi import FastAPI, Response, Body         # FastAPI
#from typing import Union, Annotated                 # typing, anotacionesiones de tipos (para ejemplos OpenAPI)

from qiskitJob import run as qiskit_run, results as qiskit_results

# Define a FastAPI app with a GET shor method

api = FastAPI()

@api.get("/")
async def root() :
    return "Implemented with FastAPI. See /docs for details"

# GET with query parameters (qpu and shots)
@api.get("/qftAdder")                      
async def qftAdder(qpu : str = "simulator", shots : int = 5000) : 

    qpus = ["simulator", "least_busy_QPU", "ibm_sherbrooke", "ibm_brisbane", "ibm_kyiv"]

    if qpu not in qpus:
        return "QPU not found", 400

    # call the run function from gate_Qiskit.py
    response = qiskit_run(qpu, shots)

    return response

@api.get("/results")                      
async def results(job_id : str) :   # either empty or the job_id of a job run on the Quantum Platform

    response = qiskit_results(None, job_id)

    return response


# if __name__ == '__main__':
#    app.run(host="localhost", port=8000)
