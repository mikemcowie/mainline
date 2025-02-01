from dataclasses import asdict, dataclass

from dominate import tags as t  # type: ignore


@dataclass
class RemoteStyleSheet:
    """Represents a stylesheet at a remote CDN url
    that will be inclueded in the rendered page
    """

    TAG_TYPE = t.link
    id: str
    href: str
    integrity: str
    rel: str = "stylesheet"
    crossorigin: str = "anonymous"

    def as_tag(self):
        return self.TAG_TYPE(**asdict(self))
