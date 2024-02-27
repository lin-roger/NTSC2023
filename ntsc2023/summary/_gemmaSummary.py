from typing import Union, List
from ..tool._Para import Para
from . import _summaryStrategy
from guidance import models, gen
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import logging

logger = logging.getLogger(__name__)


class GemmaSummary(_summaryStrategy.SummaryStrategy):
    def __init__(self) -> None:
        super().__init__()
        print(__name__)
        logger.info("gemmaSummary init...")
        tokenizer = AutoTokenizer.from_pretrained(
            "google/gemma-2b-it",
        )
        model = AutoModelForCausalLM.from_pretrained(
            "google/gemma-2b-it",
            device_map="auto",
            torch_dtype=torch.float16,
            attn_implementation="sdpa",
        )

        self.lm = models.Transformers(model, tokenizer, echo=False)
        logger.info("gemmaSummary init done...")

    def summary(self, contextData: Union[str, List[Para]]) -> Union[str, List[Para]]:
        super().summary()
        if isinstance(contextData, list):
            tmp = []
            for i in contextData:
                tmp.append(
                    Para(
                        index=i.index,
                        stratTime=i.stratTime,
                        endTime=i.endTime,
                        context=self._prompt(i.context),
                    )
                )
            return tmp
        else:
            return self._prompt(contextData)

    def _prompt(self, article: str) -> str:
        # f"""\nSummarize this text by a sentence.\nText: {contextData}\nOutput: {gen(name="output", stop=".")}"""
        prompt = f"""\
            Describe the article in one short sentence.
            Article: {article}
            Summary: The article discusses the 
            """
        # prompt = f"""\
        #     The following examples show how to summarise an article to a sentence.
        #     Article: {article}
        #     Summary:
        #     """
        lm = self.lm + prompt
        lm += gen(name="output", stop=".", max_tokens=100)
        return lm["output"].strip()
