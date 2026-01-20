from pydantic import BaseModel, Field
from typing import Union, Any      # typing, anotacionesiones de tipos (para ejemplos OpenAPI)

qpus = ["simulator", "least_busy_QPU", "ibm_fez", "ibm_torino", "ibm_marrakesh"]

class Job(BaseModel):
     job_id: Union[str, None] = Field(default=None, examples=["cwkzfrf31we00088d18g", "cwkzfrf31we00088d18g"])
     backend: Union[str, None] = Field(default="simulator", examples=qpus)
     status: Union[str, None] = Field(default=None, examples=["PENDING"])
     shots: int = Field(default=5000)
     counts: Union[Any, None] = Field(default=None)
