import csv
import sys


class CSVMealLogWriter:
    def writer(self, book):
        csv_writer = csv.writer(sys.stdout, lineterminator='\n')