from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from pytube import YouTube
from ._strReader import StrReader
from ._reader import Reder


class YoutubeReader(Reder):
    def __init__(self, url: str, windosSize=3) -> None:
        formatter = SRTFormatter()
        transcript = YouTubeTranscriptApi.get_transcript(YouTube(url).video_id)
        self.transcript = list(
            map(
                lambda x: x.strip(),
                formatter.format_transcript(transcript).splitlines(True),
            )
        )
        self._reder = StrReader(self.transcript, windosSize)

    def segmentBy(self, alg) -> None:
        self._reder.segmentBy(alg)

    def getPara(self, var: float):
        return self._reder.getPara(var)
