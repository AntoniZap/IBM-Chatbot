# Document loading and the linke
import os
import csv
from typing import Dict, List, Optional, Generator
from langchain.document_loaders.base import BaseLoader
from langchain.docstore.document import Document

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

    def get_csv(self):
      csvfile = self.add_unique_identifier()
      return csvfile  

# Loads a CSV File into a list of documents
# Each document represents one row of the CSV file. Every row is converted into a
# key/value pair and outputted to a new line in the document's page_content.
class CSVLoader(BaseLoader):
    def __init__(
        self,
        file_path = str,
        source_column: Optional[str] = None,
        metadata_columns: Optional[List[str]] = None,
        csv_args: Optional[Dict] = None,
        encoding: Optional[str] = None,
    ):
        self.file_path = file_path
        self.source_column = source_column
        self.encoding = encoding
        self.csv_args = csv_args or {}
        self.metadata_columns = metadata_columns
        
    def load(self) -> List[Document]:
        # Load data into document objects
        docs = []
        with open(self.file_path, newline="", encoding="utf8") as csvfile:
            csv_reader = csv.DictReader(csvfile, **self.csv_args)
            for i, row in enumerate(csv_reader):
                content = ""
                for k, v in row.items():
                    if((k == "reviews.text") or (k == "name")):
                        content = content + "".join(f"{k.strip()}: {v.strip()}\n")
                try:
                    source = (
                        row[self.source_column]
                        if self.source_column is not None
                        else self.file_path
                    )
                except KeyError:
                    raise ValueError(
                        f"Source column '{self.source_column}' not found in CSV file."
                    )
                metadata = {"source": source, "row": i}
                if self.metadata_columns:
                    for k, v in row.items():
                        if k in self.metadata_columns:
                            metadata[k] = v
                doc = Document(page_content=content, metadata=metadata)
                docs.append(doc)
        return docs

class ChunkedCSVLoader(CSVLoader):
    def __init__(self, file_path, chunk_size=1000, **kwargs):
        super().__init__(file_path=file_path, **kwargs)
        self.chunk_size = chunk_size
        self.chunks = []

    def load_chunks(self, start_chunk_index=0) -> Generator[List[Document], None, None]:
        with open(self.file_path, newline="", encoding="utf8") as csvfile:
            csv_reader = csv.DictReader(csvfile, **self.csv_args)
            chunk = []
            for i, row in enumerate(csv_reader):
                content = ""
                for k, v in row.items():
                    if (k == "reviews.text") or (k == "name"):
                        content += f"{k.strip()}: {v.strip()}\n"
                
                source = row[self.source_column] if self.source_column else self.file_path
                title = row.get("reviews.title", "")
                rating = row.get("reviews.rating", "")
                
                metadata = {"source": source, "row": i, "reviews.title": title, "reviews.rating": rating}
                
                doc = Document(page_content=content, metadata=metadata)

                if i >= start_chunk_index * self.chunk_size:
                    chunk.append(doc)

                if len(chunk) == self.chunk_size:
                    yield chunk
                    self.chunks.append(chunk)
                    chunk = []

            if chunk:
                yield chunk
                self.chunks.append(chunk)

    def load(self) -> List[Document]:
        for chunk in self.load_chunks():
            # Process each chunk if needed
            pass

    def get_chunks(self) -> List[List[Document]]:
        return self.chunks