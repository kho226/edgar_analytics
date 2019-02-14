from datetime import datetime, timedelta


class Parser(object):
    def __init__(self, **kwargs):
        self.locations = {
            "ip" : self._get_location(kwargs.get("header"), "ip"),
            "date" : self._get_location(kwargs.get("header"), "date"),
            "time" : self._get_location(kwargs.get("header"), "time"),
            "cik" : self._get_location(kwargs.get("header"), "cik"),
            "accession" : self._get_location(kwargs.get("header"), "accession"),
            "extention" : self._get_location(kwargs.get("header"), "extention"),
        }
    
    def _get_location(self, line, str):
        s = line.split(',')
        return s.index(str)
    
    def ip(self, line):
        return line[self.locations["ip"]]
    
    def date(self, line):
        return line[self.locations["date"]]
    
    def time(self, line):
        return line[self.locations["time"]]
    
    def cik(self, line):
        return line[self.locations["cik"]]
    
    def accession(self, line):
        return line[self.locations["accession"]]
    
    def extention(self, line):
        return line[self.locations["extention"]]
        