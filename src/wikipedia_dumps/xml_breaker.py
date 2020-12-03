# XML Breaker from https://gist.github.com/nicwolff/b4da6ec84ba9c23c8e59
# with tweaked functionality for Python 3
# and tweaked for our purposes

import os
from xml.sax import parse
from xml.sax.saxutils import XMLGenerator
from config.config import source_file_name, source_file_path, out_dir


class CycleFile(object):

    def __init__(self, directory, filename):
        self.basename, self.ext = os.path.splitext(filename)
        self.out_dir = directory
        self.index = 0
        self.open_next_file()

    def open_next_file(self):
        self.index += 1
        self.file = open(os.path.join(self.out_dir, self.name()), 'wb')

    def name(self):
        return f"{self.basename}{self.index}{self.ext}"

    def cycle(self):
        self.file.close()
        self.open_next_file()

    def write(self, str):
        self.file.write(str)

    def close(self):
        self.file.close()


class XMLBreaker(XMLGenerator):

    def __init__(self, break_into=None, break_after=1000, out=None, *args, **kwargs):
        XMLGenerator.__init__(self, out, encoding='utf-8', *args, **kwargs)
        self.out_file = out
        self.break_into = break_into
        self.break_after = break_after
        self.context = []
        self.count = 0

    def startElement(self, name, attrs):
        XMLGenerator.startElement(self, name, attrs)
        self.context.append((name, attrs))

    def endElement(self, name):
        XMLGenerator.endElement(self, name)
        self.context.pop()
        if name == self.break_into:
            self.count += 1
            if self.count == self.break_after:
                self.count = 0
                for element in reversed(self.context):
                    self.out_file.write("\n".encode('utf-8'))
                    XMLGenerator.endElement(self, element[0])
                self.out_file.cycle()
                XMLGenerator.startDocument(self)
                for element in self.context:
                    XMLGenerator.startElement(self, *element)


parse(source_file_path, XMLBreaker('page', 15000, out=CycleFile(out_dir, source_file_name)))
