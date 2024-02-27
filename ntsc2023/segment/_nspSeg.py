from . import _segStrategy
from typing import Union

import torch
from transformers import AutoTokenizer, BertForNextSentencePrediction

device = "cuda:0" if torch.cuda.is_available() else "cpu"


class NSPSeg(_segStrategy.SegStrategy):
    def __init__(self):
        super().__init__()
        self._tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self._model = BertForNextSentencePrediction.from_pretrained(
            "bert-base-uncased"
        ).to(device)
        self.softmax = torch.nn.Softmax(dim=1).to(device)

    def segment(self, s1: str, s2: str, var=None) -> Union[float, bool]:
        super().segment(s1, s2, var)
        encoding = self._tokenizer(s1, s2, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = self._model(**encoding).logits
            softOut = self.softmax(outputs)
            if var is not None:
                return bool(softOut[0, 0] > var)
            return float(softOut[0, 0])


# if __name__ == "__main__":
#     s1 = "In Italy, pizza served in formal settings, such as at a restaurant, is presented unsliced."
#     s2 = "The sky is blue due to the shorter wavelength of blue light."
#     seg = nspSeg()
#     print(seg.segment(s1, s2))
#     print(seg.segment("There's a kid on a skateboard.", "A kid is skateboarding."))
#     print(seg.segment("There's a kid on a skateboard.", "A kid is inside the house."))
