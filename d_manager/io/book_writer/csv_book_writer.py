import csv
import sys


class CSVFoodBookWriter:
    def write(self, book):
        csv_writer = csv.writer(sys.stdout, lineterminator='\n')

        is_first = True
        for food in book.generator():
            if is_first:
                csv_writer.writerow(food.get_label_of_list())
                is_first = False

            csv_writer.writerow(food.to_list())

class CSVMealLogWriter:
    def writer(self, book):
        csv_writer = csv.writer(sys.stdout, lineterminator='\n')