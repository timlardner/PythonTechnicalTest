
# coding: utf-8

import pandas as pd
import datetime
import unittest

class InstructionParser:
    def __init__(self,instruction_file):
        self.AED_SAR_weekdays = [6, 0, 1, 2, 3]
        self.weekdays = [0, 1, 2, 3, 4]
        self.df=pd.read_csv(instruction_file)
        self.fixSettlementDates()
    
    def getWorkingDay(self,day_of_week,currency):
        if currency == 'AED' or currency == 'SAR':
            if day_of_week in self.AED_SAR_weekdays:
                return day_of_week
            else:
                return self.AED_SAR_weekdays[0]
        else:
            if day_of_week in self.weekdays:
                return day_of_week
            else:
                return self.weekdays[0]+7
    
    def checkSettlement(self,settlement_date,instruction_date,currency):
        datetime_settlement = datetime.datetime.strptime(settlement_date, '%d-%b-%y')
        datetime_instruction = datetime.datetime.strptime(instruction_date, '%d-%b-%y')
        if datetime_settlement < datetime_instruction:
            datetime_settlement = datetime_instruction
        weekday_of_settlement = datetime_settlement.weekday()
        settlement_working_day = self.getWorkingDay(weekday_of_settlement,currency)
        days_to_shift = settlement_working_day - weekday_of_settlement
        actual_date = datetime_settlement + datetime.timedelta(days=days_to_shift)
        return actual_date
    
    def fixSettlementDates(self):
        self.df['ActualSettlement'] = 0
        for idx,row in self.df.iterrows():
            Currency = row['Currency']
            Settlement = row['SettlementDate']
            Instruction = row['InstructionDate']
            ActualSettlement = self.checkSettlement(Settlement,Instruction,Currency)
            self.df.loc[idx,'ActualSettlement'] = datetime.datetime.strftime(ActualSettlement,'%d-%b-%y')
    
    def calculateUSD(self):
        self.df['USD'] = 0
        for idx,row in self.df.iterrows():
            PPU = row['PricePerUnit']
            Units = row['Units']
            AFX = row['AgreedFx']
            USD = PPU * Units * AFX
            if row['Buy/Sell'] == 'B':
                USD = USD*-1
            self.df.loc[idx,'USD'] = USD

    def printDayReports(self):
        days_with_trades = self.df.ActualSettlement.unique()
        new_df = pd.DataFrame(index=days_with_trades,columns=['Incoming','Outgoing'])
        new_df = new_df.fillna(0)
        for day in days_with_trades:
            incoming=0
            outgoing=0
            cols = self.df.loc[self.df['ActualSettlement'] == day]
            for col in cols['USD']:
                if col < 0:
                    incoming = incoming + col*-1
                else:
                    outgoing = outgoing + col
            new_df.loc[day,'Incoming'] = incoming
            new_df.loc[day,'Outgoing'] = outgoing
        new_df = new_df.sort_index()
        print(new_df)
        print('\n')
        return new_df 

    def printEntityReports(self):
        unique_entities = self.df.Entity.unique()
        new_df = pd.DataFrame(index=unique_entities,columns=['Incoming','Outgoing'])
        new_df = new_df.fillna(0)
        for idx,row in self.df.iterrows():
            ent = row['Entity']
            usd = row['USD']
            if usd<0:
                new_df.loc[ent,'Incoming'] = new_df.loc[ent,'Incoming'] + usd*-1
            else:
                new_df.loc[ent,'Outgoing'] = new_df.loc[ent,'Outgoing'] + usd
        best_incoming = new_df.sort_values('Incoming',ascending=False).drop('Outgoing',1)
        print(best_incoming)
        print('\n')
        best_outgoing = new_df.sort_values('Outgoing',ascending=False).drop('Incoming',1)
        print(best_outgoing)
        return best_incoming,best_outgoing

    # Test function. Print the dataframe.
    def printTable(self):
        print(self.df)
        
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

    # Ensure that we're summing correctly for multiple transactions on one date.
    def test_day_reporting(self):
        filename = "SimpleData.csv"
        Parser = InstructionParser(filename)
        Parser.calculateUSD()
        DayReport = Parser.printDayReports()
        self.assertEqual(DayReport.loc['06-Mar-17','Incoming'],5)
        self.assertEqual(DayReport.loc['06-Mar-17','Outgoing'],2)
        self.assertEqual(DayReport.loc['05-Mar-17','Incoming'],2)
        self.assertEqual(DayReport.loc['05-Mar-17','Outgoing'],0)

    # Check that we're summing correctly for multiple occurrences of the same entity in our list
    # of transactions.
    def test_entity_reporting(self):
        filename = "SimpleData.csv"
        Parser = InstructionParser(filename)
        Parser.calculateUSD()
        best_incoming,best_outgoing = Parser.printEntityReports()
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





