# Document loading and the linke
from langchain_community.document_loaders.csv_loader import CSVLoader

class csv_to_langchain:
    def amazon_reviews():
        loader = CSVLoader(file_path='Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv', source_column='reviews.text', encoding='8859')

        amazonReviewData = loader.load()

        return amazonReviewData
