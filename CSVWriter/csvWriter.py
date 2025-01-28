import csv

class CSVWriter:
    
    def write_to_csv(csv_file, *args):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Variable Name", "Value"])
            for variable in args:
                writer.writerow([variable[0], variable[1]])