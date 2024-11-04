
# ejecutar con    python -m uvicorn main:api --reload --host 0.0.0.0 --port 8000

from fastapi import FastAPI, Response, Body         # FastAPI
from typing import Annotated                        # typing, anotacionesiones de tipos (para ejemplos OpenAPI)

from job import Job, qpus
from qiskitJob import run as job_run, results as job_results, plot as job_plot

# Define a FastAPI app with a GET shor method

api = FastAPI()

@api.get("/")
async def root() :
    return "Implemented with FastAPI. See /docs for details"

# POST a qftAdder Job with qpu and shots in body
@api.post("/jobs/qftAdder", status_code=201)                      
async def qftAdder(job: Annotated[Job, 
                        Body(examples=[{"backend" : "simulator",
                                        "shots": 1000},
                                       {"backend" : "ibm_sherbrooke",
                                        "shots": 5000}]
                        )]):

    if job.backend not in qpus:
        return { "error" : "QPU not found in " + str(qpus)}, 400

    response = job_run(job)

    return response

# GET the results of a Job (of any kind)
@api.get("/jobs/{job_id}")                      
async def results(job_id : str): # Annotated[str,examples=["cwkzfrf31we00088d18g","cwkxypj31we00088cy7g"]]):
    
    response = job_results(job_id)

    return response

# POST to show a plotter with job details as body parameters
#      probably it should be a QUERY request, if it is finally implemented
#
@api.post("/plots", status_code=201)                      
async def plot(job : Annotated[Job, 
                     Body(examples=[{"job_id": "cwkzfrf31we00088d18g",
                                     "backend" : "ibm_brisbane",
                                     "status" : "Done",
                                     "shots": 10000,
                                     "counts": {"1000": 25, "1001": 41, "1010": 12, "1011": 72, "1100": 7, "1101": 23, "1110": 24,
                                                "1111": 136, "0011": 115, "0111": 394, "0101": 55, "0110": 49, "0100": 8, "0001": 21,
                                                "0000": 13, "0010": 5}}]
                         )]):
    
    response = job_plot(job)
    return response

# if __name__ == '__main__':
#    app.run(host="localhost", port=8000)
