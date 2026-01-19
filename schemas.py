from pydantic import BaseModel, ConfigDict

class ShowDepartment(BaseModel):
    id :int
    nom :str 
    model_config = ConfigDict(from_attributes=True)
