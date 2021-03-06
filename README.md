# PythonTechnicalTest

[![Build Status](https://travis-ci.org/timlardner/PythonTechnicalTest.svg?branch=master)](https://travis-ci.org/timlardner/PythonTechnicalTest)

Usage: Create an instance of the *InstructionParser* class passing the path to a .csv file as the only argument.

For example, run:

    from TechnicalTest import InstructionParser

    Parser = InstructionParser('Transactions.csv')
    Parser.printAllReports()
    
to print all reports. Subsections of reports can be printed individually using:

    Parser = InstructionParser('Transactions.csv')
    Parser.calculateUSD()
    Parser.printDayReports()
    Parser.printEntityReports()
    
Unit tests is available in the *UnitTesting.py* source file and CI is enabled on this project via TravisCI. Multiple .csv files have been included in this repoistory for the purposes of testing.
