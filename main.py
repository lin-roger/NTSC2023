from typing import List
from fastapi import FastAPI
from ntsc2023.tool import _strReader
from ntsc2023.segment import _nspSeg
from ntsc2023.summary import _gemmaSummary
from ntsc2023.tool._Para import Para

segAlg = _nspSeg()
sumAlg = _gemmaSummary()
app = FastAPI()


@app.get("/segment/{path}")
def read_segment(path: str) -> List[Para]:
    data = _strReader("./datapool/tmp.srt")
    data.segmentBy(segAlg)
    return sumAlg.summary(data.getPara(0.7))


# @app.get("/summary/{alg}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
