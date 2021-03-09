from collections import namedtuple
import textwrap

Author = namedtuple('Author', ['name', 'link', 'pic_link'], defaults=['', ''])


class Comment(namedtuple('Comment', ['author', 'link', 'text', 'date'], defaults=['', '', ''])):
    def __str__(self):
        return str(self.author.name) + ' <' + str(self.link) + '>:\n' + textwrap.indent(textwrap.fill(self.text), '\t')

    def get_text(self):
        return self.text
