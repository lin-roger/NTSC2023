# %%
from ntsc2023 import tool
from ntsc2023 import segment
from ntsc2023 import summary
import torch

# %%
alg = segment.MixSeg()
# data = tool.StrReader("./datapool/tmp.srt")
data = tool.YoutubeReader("https://youtu.be/mCjRYS1Wr0Q?si=vkiZxxe6o1kuYatN")
data.segmentBy(alg)
# %%
del alg
torch.cuda.empty_cache()
# %%
sumAlg = summary.GemmaSummary()
# print(data._getParaSegIdxList(0.5))
sumAlg.summary(data.getPara(1.0))

# for i in np.arange(0.0, 2.0, 0.05):
#     print(len(data.getPara(i)))

# %%

