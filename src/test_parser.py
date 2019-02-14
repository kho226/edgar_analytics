from parser import Parser
from datetime import timedelta, datetime

import unittest
from unittest import TestCase

class parserTestCase(TestCase):
    def setUp(self):
        self.header = "ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser" #noqa
        self.test = "101.81.133.jja,2017-06-30,00:00:00,0.0,1608552.0,0001047469-17-004337,-index.htm,200.0,80251.0,1.0,0.0,0.0,9.0,0.0,"#noqa
        self.p = Parser(
            header = self.header
        )

    def test_init(self):
        self.assertEqual(self.p.locations["ip"],0)
        self.assertEqual(self.p.locations["date"],1)
        self.assertEqual(self.p.locations["time"],2)
    
    def test_get_location(self):
        test = self.p._get_location(self.header, "ip")
        self.assertEqual(test,0)
        test = self.p._get_location(self.header, "accession")
        self.assertEqual(test,5)
    
    def test_ip(self):
        test = self.p.ip(self.test.split(","))
        self.assertEqual("101.81.133.jja", test)
    
    def test_date(self):
        test = self.p.date(self.test.split(","))
        self.assertEqual("2017-06-30", test)
    
    def test_time(self):
        test = self.p.time(self.test.split(","))
        self.assertEqual("00:00:00", test)
    
    def test_cik(self):
        test = self.p.cik(self.test.split(","))
        self.assertEqual("1608552.0", test)
    
    def test_accession(self):
        test = self.p.accession(self.test.split(","))
        self.assertEqual("0001047469-17-004337", test)
    
    def test_extention(self):
        test = self.p.extention(self.test.split(","))
        self.assertEqual("-index.htm", test)
    
    

if __name__ == "__main__":
    unittest.main()