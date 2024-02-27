from pydantic import BaseModel


class Para(BaseModel):
    index: int
    stratTime: str
    endTime: str
    context: str


#     {
#     "index": tmp["index"][0],
#     "stratTime": tmp["stratTime"][0],
#     "endTime": tmp["endTime"][-1],
#     "context": " ".join(tmp["context"]),
# }