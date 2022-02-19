import dataclasses


@dataclasses.dataclass
class Author:
    name: str
    link: str
    pic_link: str

    def __hash__(self):
        return hash(str(self))

    def as_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Comment:
    author: Author
    link: str
    text: str
    date: str

    def as_dict(self):
        return dataclasses.asdict(self)
