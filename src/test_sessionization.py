import sessionization
from sessionization import Sessionizer
import unittest
from unittest import TestCase
from datetime import timedelta, datetime


class sessionizationTestCase(TestCase):
    def setUp(self):
        self.header = "ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser" #noqa
        self.s = Sessionizer(
            infile="test",
            outfile="test",
            inactivity_period=0,
            header = self.header
        )

    def test_init(self):
        self.assertEqual(self.s.infile, "test")
        self.assertEqual(self.s.outfile, "test")
        self.assertEqual(self.s.inactivity_period, timedelta(seconds=0))
    
    def test_have_seen(self):
        test = self.s.have_seen("not_seen")
        return self.assertEqual(test, False)
    
    def test_is_expired(self):
        test = self.s.is_expired(timedelta(seconds=2))
        self.assertEqual(test, True)
    
    def test_upsert_record(self):
        start_time = datetime.now()
        end_time = datetime.now() + timedelta(seconds = 10)
        ip = "127.0.0.01"
        cik  = "1"
        accession = "2"
        extention = "3"

        self.s.upsert_in_record(
            start_time = start_time,
            end_time = end_time,
            ip = ip,
            cik = cik,
            accession = accession,
            extention = extention
        )
        expected = {
            "start_time" : start_time,
            "visited" : set({"{}{}{}".format(cik, accession, extention)}),
            "end_time" : end_time
        }
        self.assertEqual(self.s.in_record[ip]["visited"],expected["visited"])
        self.assertEqual(self.s.in_record[ip]["start_time"], expected["start_time"])
    
    def test_insert_out_record(self):
        elapsed_time = timedelta(hours=1)
        start_time = datetime.now()
        end_time = datetime.now() + timedelta(seconds = 10)
        ip = "127.0.0.01"
        cik  = "1"
        accession = "2"
        extention = "3"
        self.s.upsert_in_record(
            start_time = start_time,
            end_time = end_time,
            ip = ip,
            cik = cik,
            accession = accession,
            extention = extention
        )
        self.s.insert_out_record(
            elapsed_time = elapsed_time,
            ip = ip
        )
        self.assertEquals(
            self.s.out_record[ip]["end_time"],
            self.s.in_record[ip]["start_time"])
    
    def test_terminate_open_sessions(self):
        elapsed_time = timedelta(hours=1)
        start_time = datetime.now()
        end_time = datetime.now() + timedelta(seconds = 10)
        ip = "127.0.0.01"
        cik  = "1"
        accession = "2"
        extention = "3"
        self.s.upsert_in_record(
            start_time = start_time,
            end_time = end_time,
            ip = ip,
            cik = cik,
            accession = accession,
            extention = extention
        )
        self.s.terminated_open_sesssions()
        self.assertEqual(self.s.out_record[ip]["end_time"], start_time)

    def test_calculate_visits(self):
        elapsed_time = timedelta(hours=1)
        start_time = datetime.now()
        end_time = datetime.now() + timedelta(seconds = 10)
        ip = "127.0.0.01"
        cik  = "1"
        accession = "2"
        extention = "3"
        self.s.upsert_in_record(
            start_time = start_time,
            end_time = end_time,
            ip = ip,
            cik = cik,
            accession = accession,
            extention = extention
        )
        self.s.terminated_open_sesssions()
        self.s.calculate_visits()
        self.assertEquals(self.s.out_record[ip]["duration"], timedelta(0))

if __name__ == "__main__":
    unittest.main()