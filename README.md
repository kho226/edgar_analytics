# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Run Instructions](README.md#run-instructions)
4. [Test Instructions](README.md#test-instructions)


# Problem

Many investors, researchers, journalists and others use the Securities and Exchange Commission's Electronic Data Gathering, Analysis and Retrieval (EDGAR) system to retrieve financial documents, whether they are doing a deep dive into a particular company's financials or learning new information that a company has revealed through their filings.

The SEC maintains EDGAR weblogs showing which IP addresses have accessed which documents for what company, and at what day and time this occurred.

Imagine the SEC has asked you to take the data and produce a dashboard that would provide a real-time view into how users are accessing EDGAR, including how long they stay and the number of documents they access during the visit.

While the SEC usually makes its EDGAR weblogs publicly available after a six month delay, imagine that for this challenge, the government entity has promised it would stream the data into your program in real-time and with no delay.

Your job as a data engineer is to build a pipeline to ingest that stream of data and calculate how long a particular user spends on EDGAR during a visit and how many documents that user requests during the session.



# Approach
```
      ├── input
      │   └──inactivity_period.txt
      │   └──log.csv
      ├── insight_testsuite
      │   └── ...
      ├── output
      │   └──sessinization.txt
      ├── src
      │   └──parser.py
      │   └──test_parser.py
      │   └──sessionization.py
      │   └──test_sessionization.py  
      ├── README.md
      ├── run.sh

      
```
data flows through sessionizer.py and written to output.txt
 

# Run-Instructions

# Test-Instructions
