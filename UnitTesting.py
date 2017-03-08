import unittest
from TechnicalTest import InstructionParser

class ParserTest(unittest.TestCase):
    # Ensure that we can actually load the .csv file and read records from it.
    def test_check_csv_record_load(self):
        filename = "SimpleData.csv"
        Parser = InstructionParser(filename)
        self.assertEqual(len(Parser.df['Entity']),4)

    # Ensure our weekday checker is functioning correctly.
    def test_weekday_for_both_weekends(self):
        filename = "SimpleData.csv"
        Parser = InstructionParser(filename)
        self.assertEqual(Parser.df.ActualSettlement[0],'06-Mar-17')
        self.assertEqual(Parser.df.ActualSettlement[1],'05-Mar-17')

    def get_simple_parser(self):
        filename = "SimpleData.csv"
        Parser = InstructionParser(filename)
        Parser.calculateUSD()
        return Parser

    # Ensure that we're summing correctly for multiple transactions on one date.
    def test_day_reporting(self):
        DayReport = self.get_simple_parser().printDayReports()
        self.assertEqual(DayReport.loc['06-Mar-17','Incoming'],5)
        self.assertEqual(DayReport.loc['06-Mar-17','Outgoing'],2)
        self.assertEqual(DayReport.loc['05-Mar-17','Incoming'],2)
        self.assertEqual(DayReport.loc['05-Mar-17','Outgoing'],0)

    # Check that we're summing correctly for multiple occurrences of the same entity in our list
    # of transactions.
    def test_entity_reporting(self):
        best_incoming,best_outgoing = self.get_simple_parser().printEntityReports()
        self.assertEqual(best_incoming.loc['Test','Incoming'],5)
        self.assertEqual(best_outgoing.loc['Test','Outgoing'],2)
        self.assertEqual(best_incoming.loc['Foobar','Incoming'],2)
        self.assertEqual(best_outgoing.loc['Foobar','Outgoing'],0)

    # Check the known results from the given dataset.
    def test_given_csv(self):
        filename = "SampleData.csv"
        Parser = InstructionParser(filename)
        Parser.calculateUSD()
        DayReport = Parser.printDayReports()
        best_incoming,best_outgoing = Parser.printEntityReports()
        self.assertEqual(best_incoming.loc['foo','Incoming'],10025.0)
        self.assertEqual(best_outgoing.loc['foo','Outgoing'],0)
        self.assertEqual(best_incoming.loc['bar','Incoming'],0)
        self.assertEqual(best_outgoing.loc['bar','Outgoing'],14899.5)
        self.assertEqual(DayReport.loc['04-Jan-16','Incoming'],10025.0)
        self.assertEqual(DayReport.loc['04-Jan-16','Outgoing'],0)
        self.assertEqual(DayReport.loc['07-Jan-16','Incoming'],0)
        self.assertEqual(DayReport.loc['07-Jan-16','Outgoing'],14899.5)

    # We want to ensure that our date report is printed in order. Here we get the index of our data
    # frame, then sort it using the built-in function. These lists should be identical.
    def test_date_order(self):
        filename = "DateTest.csv"
        Parser = InstructionParser(filename)
        Parser.calculateUSD()
        DayReport = Parser.printDayReports()
        vals = DayReport.index.values.tolist()
        test = vals == sorted(vals)
        self.assertEqual(test,True)

    # We've got a settlement before the instruction in DateTest.csv. It also occurs on a weekend.
    # We expect the settlement date to be moved to the instruction date then moved again when the
    # weekend check is evaluated. The date should be moved to 13th March, which will be the only
    # occurrence of this date.
    def test_settlement_before_instruction(self):
        filename = "DateTest.csv"
        Parser = InstructionParser(filename)
        Parser.calculateUSD()
        DayReport = Parser.printDayReports()
        self.assertEqual('13-Mar-17' in DayReport.index.values,True)

if __name__ == '__main__':
    unittest.main()