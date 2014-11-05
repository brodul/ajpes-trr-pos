raise NotImplementedError("This app is still in development")
import xml.etree.ElementTree as et
import logging

from sqlalchemy import create_engine
import dateutil.parser

from models import (
    DBSession,
    Base,
    Racun,
    Imetnik,
    Naslov
)


# engine = create_engine("postgresql://brodul:test@localhost/test")
engine = create_engine("sqlite://")
__version__ = '0.1.0'

get_version = lambda: __version__

DBSession.remove()
DBSession.configure(bind=engine)

Base.metadata.bind = engine
Base.metadata.create_all(engine)

data_file = '../data/RTR_AJPES_20140831_POS_P_M.xml'


class XMLParser(object):
    """
    http://boscoh.com/programming/reading-xml-serially.html
    """

    def __init__(self, input_file, encoding='utf-8'):

        # open the xml file for iteration
        self.context = et.iterparse(
            input_file,
            events=(
                "start",
                "end",
                'start-ns',
                'end-ns'
            )
        )
        self.event, self.elem = None, None
        self._goto_first()
        self.counter = 0

    def __repr__(self):
        return "Iterator at " + repr((self.event, self.elem))

    def filter_text(self, text):
        text = None and text.strip()

        return text

    def next_event(self):
        self.event, self.elem = \
            self.raw_event, self.raw_elem = self.context.next()

        # set elem_text
        if not isinstance(self.elem, tuple):
            self.elem_text = self.filter_text(self.elem.text)
        else:
            self.elem_text = None

        return self.event, self.elem

    @property
    def tag(self):
        return self.elem.tag.split('}')[1]

    def _goto_first(self):
        self.event, self.elem = self.next_event()
        while not (self.event == 'start' and self.elem.tag.endswith('Tr')):
            self.event, self.elem = self.next_event()

    def parse_tag_text(self,  tag_name, attr):

        assert self.tag == tag_name
        assert self.event == 'start'
        attr[tag_name] = self.elem.text
        self.next_event()
        assert self.tag == tag_name
        assert self.event == 'end'

    def parse_tr(self):
        import sys

        while not (self.tag == 'RtrPod' and self.event == 'end'):
            self.counter += 1

            if not self.counter % 10:
                DBSession.commit()
                sys.stdout.write('.')
                sys.stdout.flush()
            assert self.tag == 'Tr'
            assert self.event == 'start'
            tr_elem = self.elem
            self.tr = dict(self.elem.attrib)
            self.tr['dSpre'] = dateutil.parser.parse(self.tr.get('dSpre'))
            self.tr['dOdprt'] = dateutil.parser.parse(self.tr.get('dOdprt'))

            self.next_event()
            while self.tag == 'Imetnik' and self.event == 'start':
                self.parse_imetnik()
                self.next_event()

            while self.tag in ('PopolnoImeRacuna', 'KratkoImeRacuna', 'NazivPp'):
                self.parse_tag_text(self.tag, self.tr)
                self.next_event()

            while self.tag == 'Imetnik' and self.event == 'start':
                self.parse_imetnik()
                self.next_event()

            assert self.tag == 'Tr'
            assert self.event == 'end'

            self.next_event()
            tr_elem.clear()
            if self.imetnik.get('davcna'):
                naslov = Naslov(**self.naslov)
                DBSession.add(naslov)
                imetnik = Imetnik(naslovi=[naslov], **self.imetnik)
                DBSession.merge(imetnik)
                racun = Racun(imetniki=[imetnik], **self.tr)
                DBSession.merge(racun)
            else:
                logging.warning("Podjetje: %s nima davcne", self.imetnik['PopolnoIme'])
            yield self.tr

    def parse_imetnik(self):
        assert self.tag == 'Imetnik'
        assert self.event == 'start'
        while not (self.tag == "Imetnik" and self.event == "end"):
            # can be multiple
            self.imetnik = dict(self.elem.attrib)
            self.next_event()
            while self.tag in ('PopolnoIme', 'KratkoIme'):
                self.parse_tag_text(self.tag, self.imetnik)
                self.next_event()

            while self.tag == 'Naslov' and self.event == 'start':
                self.parse_naslov()
                self.next_event()

        assert self.tag == 'Imetnik'
        assert self.event == 'end'

    def parse_naslov(self):
        assert self.tag == 'Naslov'
        assert self.event == 'start'
        while not (self.tag == "Naslov" and self.event == "end"):
            # can be multiple
            self.naslov = dict(self.elem.attrib)
            self.next_event()

            while self.tag in ('Drzava', 'Obcina', 'Posta', 'Ulica', 'Naselje'):
                self.parse_tag_text(self.tag, self.naslov)
                self.next_event()

        assert self.tag == 'Naslov'
        assert self.event == 'end'

    def start(self):
        for d in self.parse_tr():
            pass
        print self.counter

xmlparser = XMLParser(data_file)
xmlparser.start()
