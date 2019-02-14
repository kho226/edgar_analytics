from datetime import datetime, timedelta
from parser import Parser
import csv


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
    
    
    def upsert_in_record(self, **kwargs):
        start_time = kwargs.get("start_time", None)
        end_time = kwargs.get("end_time", None)
        ip = kwargs.get("ip")
        cik = kwargs.get("cik")
        accession = kwargs.get("accession")
        extention = kwargs.get("extention")

        address = "{}{}{}".format(cik, accession, extention)
        val = self.in_record.get(ip, {})
        visited = val.get("visited", set())
        visited.add(address)
        val["visited"] = visited

        if val.get("start_time" , None) is None:
            val["start_time"] = start_time
        
        self.in_record[ip] = val
    
    def insert_out_record(self, **kwargs):
        ip = kwargs.get("ip")
        elapsed_time = kwargs.get("elapsed_time")
        val = self.in_record.get(ip, {})
        start_time = val.get("start_time", -1)
        end_time = start_time + elapsed_time if elapsed_time < self.inactivity_period else \
            start_time + self.inactivity_period
        val["end_time"] = end_time
        self.out_record[ip] = val
        

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

                self.upsert_record(
                        start_time = current_time,
                        ip = ip,
                        cik = cik,
                        accession = accession,
                        extention = extention)
    
                elapsed_time = current_time - self.in_record.get("start_time")
                if self.is_expired(elapsed_time):
                    self.insert_out_record(
                        ip=ip,
                        elapsed_time = elapsed_time
                    )
        self.terminated_open_sesssions()
        self.calculate_visits()
        self.write_to_file()
                
    def terminated_open_sesssions(self):
        for k, v in self.in_record.items():
            if k not in self.out_record:
                self.insert_out_record(
                    ip = k,
                    elapsed_time = self.inactivity_period
                )
    
    def calculate_visits(self):
        for k, v in self.out_record.items():
            duration = v.get("end_time", 0) - v.get("start_time", 0)
            self.out_record[k]["duration"] = duration
    
    def write_to_file(self):
        with open(self.outfile, "w") as fh:
            writer = csv.DictWriter(fh, field_names=["ip_address", "start_time", "end_time", "duration", "count"], delimiter=",")
            writer.writeheader()
            for k, v in self.out_record.items():
                ip = k
                start_time = v["start_time"]
                end_time = v["end_time"]
                duration = v["duration"].seconds
                count = len(v["visited"])
                out_line = "{}{}{}{}{}".format(start_time, end_time, duration, count)
                fh.write(out_line)

    
                    
