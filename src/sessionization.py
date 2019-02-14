from datetime import datetime, timedelta
from parser import Parser


class Sessionizer(object):
    def __init__(self, **kwargs):
        self.infile = kwargs.get("infile")
        self.outfile = kwargs.get("outfile")
        self.inactivity_period = timedelta(
            seconds=kwargs.get("inactivity_period"))
        self.in_record = {}
        self.out_record = {}
        self.p = Parser(
            header = kwargs.get("header")
        )
    
    def have_seen(self, ip):
        val = self.in_record.get(ip, -1)
        return val != -1
    
    def is_expired(self, timedelta):
        return timedelta >= self.inactivity_period
    
    def insert_record(self,**kwargs):
        start_time = kwargs.get("start_time")
        ip = kwargs.get("ip")
        cik = kwargs.get("cik")
        accession = kwargs.get("accession")
        extention = kwargs.get("extention")

        address = "{}{}{}".format(cik, accession, extention)

        val = self.in_record.get(ip, {})
        
        val["start_time"] = start_time

        visited = val.get("visited", set())
        visited.add(address)
        val["visited"] = visited 

        self.in_record[ip] = val

    def parse(self):
        count = 0
        with open(self.in_file, "r") as fh:
            next(fh)
            for line in fh:
                s = line.split(",")
                ip = self.p.ip(s)
                date = self.p.date(s)
                time = self.p.time(s)
                cik = self.p.cik(s)
                accession = self.p.accession(s)
                extention = self.p.extention(s)
                current_time = datetime.strptime("{}{}".format(date,time), "%Y-%m-%d%H:%M:%S")
                if self.have_seen(ip):
                    #update  record
                    val = self.in_record.get(ip, {})
                    visited = val.get("visited", set())
                    visited.add("{}{}{}".format(cik, accession, extention))
                else:
                    val = self.in_record(ip, {})
                    #insert record
                    start_time = val.get("start_time", -1)
                    start_time = current_time
                    val["start_time"] = start_time

                    visited = val.get("visited", set())
                    visted.add("{}{}{}".format(cik,accession,extention))
                    val["visited"] = visited 
                elapsed_time = current_time - self.in_record.get("start_time")
                if self.is_expired(elapsed_time):
                    # insert_record
                    val = self.in_record.get(ip, -1)
                    start_time = val.get("start_time", -1)
                    end_time = start_time + elapsed_time if elapsed_time < self.inactivity_period else \
                            start_time + self.inactivity_period
                    val["end_time"] = end_time
                    self.out_record[ip] = val


                


    