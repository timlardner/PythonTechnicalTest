# PythonTechnicalTest

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0006f38a7d38442cbf50501a2011b927)](https://www.codacy.com/app/timlardner/PythonTechnicalTest?utm_source=github.com&utm_medium=referral&utm_content=timlardner/PythonTechnicalTest&utm_campaign=badger)
[![Build Status](https://travis-ci.org/timlardner/PythonTechnicalTest.svg?branch=master)](https://travis-ci.org/timlardner/PythonTechnicalTest)

Usage: Create an instance of the *InstructionParser* class passing the path to a .csv file as the only argument.

For example, run:

    Parser = InstructionParser('Transactions.csv')
    Parser.printAllReports()
    
to print all reports. Subsections of reports can be printed individually using:

    Parser = InstructionParser('Transactions.csv')
    Parser.calculateUSD()
    Parser.printDayReports()
    Parser.printEntityReports()
    
Unit tests is available in the *UnitTesting.py* source file and CI is enabled on this project via TravisCI. Multiple .csv files have been included in this repoistory for the purposes of testing.
