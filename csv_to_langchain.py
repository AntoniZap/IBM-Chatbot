# Document loading and the linke
import os
from langchain_community.document_loaders.csv_loader import CSVLoader
import csv

class csv_to_langchain:

    def __init__(self, path):
        self.path = path

    def add_unique_identifier(self):
        with open(self.path, "r", encoding="utf-8") as input_file:
            reader = csv.reader(input_file)
            header = next(reader)
            rows = list(reader)
    
        output_filename = "New_" + os.path.basename(self.path)

        # Open the output file for writing
        with open(output_filename, "w", newline='', encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(header + ['Review_Unique_ID'])
        
            # Initialize the unique identifier - filename+rownum
            base_name = os.path.basename(self.path)
            csv_name = os.path.splitext(base_name)[0]
            unique_id = csv_name + "_1"
            counter = 1

            # Iterate over each row in the input file and add unique identifier
            for row in rows:
                row_with_id = row + [unique_id]
                writer.writerow(row_with_id)
                # Increment the unique identifier for the next row
                counter += 1
                parts = unique_id.rsplit('_', 1)
                prefix = parts[0]
                unique_id = prefix + "_" + str(counter)

        return output_filename


    def amazon_reviews(self):
        csvfile = self.add_unique_identifier() 
        
        loader = CSVLoader(file_path='Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv', source_column='reviews.text', encoding='8859')

        amazonReviewData = loader.load()

        return amazonReviewData
    




    
