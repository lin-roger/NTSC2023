from . import _segStrategy
from typing import Union

import torch
from transformers import AutoModel, AutoTokenizer
from scipy.spatial.distance import cosine

device = "cuda:0" if torch.cuda.is_available() else "cpu"


class SimSeg(_segStrategy.SegStrategy):
    def __init__(self):
        super().__init__()
        self._tokenizer = AutoTokenizer.from_pretrained(
            "princeton-nlp/sup-simcse-roberta-base"
        )
        self._model = AutoModel.from_pretrained(
            "princeton-nlp/sup-simcse-roberta-base"
        ).to(device)

    def segment(self, s1: str, s2: str, var=None) -> Union[float, bool]:
        super().segment(s1, s2, var)
        encoding = self._tokenizer(
            [s1, s2], padding=True, truncation=True, return_tensors="pt"
        ).to(device)
        with torch.no_grad():
            outputs = self._model(
                **encoding, output_hidden_states=True, return_dict=True
            ).pooler_output.cpu()
            if var is not None:
                return (1 - cosine(outputs[0], outputs[1])) > var
            else:
                return 1 - cosine(outputs[0], outputs[1])
            # return cosine(outputs[0], outputs[1]) > var


# if __name__ == "__main__":
#     s1 = "In Italy, pizza served in formal settings, such as at a restaurant, is presented unsliced."
#     s2 = "The sky is blue due to the shorter wavelength of blue light."
#     seg = simSeg()
#     print(seg.segment(s1, s2))
#     print(seg.segment("There's a kid on a skateboard.", "A kid is skateboarding."))
#     print(seg.segment("There's a kid on a skateboard.", "A kid is inside the house."))
    # if(seg.segment(s1, s2)):
    #     print("don't seg")
    # else:
    #     print("need seg")
