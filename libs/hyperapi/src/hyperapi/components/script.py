from dataclasses import asdict, dataclass, field
from typing import Literal

from dominate import tags as t  # type: ignore


@dataclass
class RemoteScript:
    """Represents a remote js
    that will be inclueded in the rendered page
    """

    TAG_TYPE = t.script
    id: str
    src: str
    integrity: str
    crossorigin: Literal["anonymous"] = field(default="anonymous", init=False)

    def as_tag(self):
        return self.TAG_TYPE(**asdict(self))
