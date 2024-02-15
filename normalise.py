import csv
from dataclasses import dataclass
from langchain_community.document_loaders import CSVLoader

class Datafiniti:
    # fields marked as "needs context" will need to have a prompt in the
    # CSV ingestion dialogue asking for more details. E.g., reviews.rating
    # will need to have information added that the number is out of 5 or 3
    # .etc.
    unwanted = [
        # use dateUpdated for all of these
        'reviews.dateSeen',
        'reviews.dateAdded',
        'dateAdded',
        'reviews.date',

        'manufacturerNumber', # irrelenvant
        
        'primaryCategories',
        'categories', # fucks up the similarity search
        
        'imageURLs', # irrelevant
        'sourceURLs', # irrelevant
        'reviews.sourceURLs', # irrelevant
        'reviews.username', # irrelevant
        'asins', # irrelevant
        'keys', # marketing (?)
        'reviews.id', # irrelevant
        'reviews.numHelpful', # needs context
        'reviews.rating', # needs context / bound for LLM (have prompt to provide this later),
        'id' # irrelevant
    ]
    
    def __init__(self, path):
        self.path = path

    def load(self):
        """
        Loads the provided CSV with the unwanted paths used as metadata returns a list of
        langchain documents for each CSV row. Uses CSVLoader internally.
        """
        loader = CSVLoader(self.path, metadata_columns=self.unwanted, encoding="utf-8-sig")
        documents = loader.load()
        return documents

    def clean(self, output_path=None):
        """
        Removes unwanted fields from a csv and writes the result to output_path, which is
        normal.{self.path} by default
        """
        reviews = []
        with open(self.path) as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = set(reader.fieldnames)
            for field in self.unwanted:
                fieldnames.remove(field)
                for review in reader:
                    for field in self.unwanted:
                        review.pop(field)
                    reviews.append(review)
            
        with open(output_path or f"normal.{self.path}", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames)
            writer.writeheader()
            for review in reviews:
                writer.writerow(review)

# TODO: Write a function / class that uses an LLM to determine which
# fields are important. The UI should provide a way of guiding the
# user through which fields are probably useless and which fields need
# more context.
