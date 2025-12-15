"""
File reader module for processing uploaded data files
Supports CSV, JSON, XML, and TXT formats
"""
import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class FileReader:
    """Base class for reading files"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def read(self) -> List[Dict[str, Any]]:
        """Read and parse file, return list of data records"""
        raise NotImplementedError


class CSVReader(FileReader):
    """CSV file reader"""
    
    def read(self) -> List[Dict[str, Any]]:
        """Read CSV file and return list of dictionaries"""
        try:
            records = []
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row:  # Skip empty rows
                        records.append(row)
            logger.info(f"Read {len(records)} records from CSV: {self.file_path}")
            return records
        except Exception as e:
            logger.error(f"Error reading CSV file {self.file_path}: {str(e)}")
            raise


class JSONReader(FileReader):
    """JSON file reader"""
    
    def read(self) -> List[Dict[str, Any]]:
        """Read JSON file and return list of dictionaries"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both single object and array of objects
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                # If it's a single object, wrap it in a list
                records = [data]
            else:
                raise ValueError("JSON must be an object or array of objects")
            
            logger.info(f"Read {len(records)} records from JSON: {self.file_path}")
            return records
        except Exception as e:
            logger.error(f"Error reading JSON file {self.file_path}: {str(e)}")
            raise


class XMLReader(FileReader):
    """XML file reader"""
    
    def read(self) -> List[Dict[str, Any]]:
        """Read XML file and return list of dictionaries"""
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            records = []
            
            # Find all item/record elements
            for item in root.findall('.//item') + root.findall('.//record') + root.findall('.//event'):
                record = {}
                for child in item:
                    # Handle nested elements by converting to string
                    if len(child) > 0:
                        record[child.tag] = ET.tostring(child, encoding='unicode')
                    else:
                        record[child.tag] = child.text
                
                # If no recognized item tags, treat all children as fields
                if not record:
                    for child in item:
                        record[child.tag] = child.text
                
                if record:
                    records.append(record)
            
            logger.info(f"Read {len(records)} records from XML: {self.file_path}")
            return records
        except Exception as e:
            logger.error(f"Error reading XML file {self.file_path}: {str(e)}")
            raise


class TXTReader(FileReader):
    """Plain text file reader (line-by-line)"""
    
    def read(self) -> List[Dict[str, Any]]:
        """Read TXT file line by line"""
        try:
            records = []
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:  # Skip empty lines
                        records.append({'line_number': line_num, 'content': line})
            
            logger.info(f"Read {len(records)} lines from TXT: {self.file_path}")
            return records
        except Exception as e:
            logger.error(f"Error reading TXT file {self.file_path}: {str(e)}")
            raise


class FileReaderFactory:
    """Factory for creating appropriate file readers"""
    
    READERS = {
        '.csv': CSVReader,
        '.json': JSONReader,
        '.xml': XMLReader,
        '.txt': TXTReader,
    }
    
    @classmethod
    def create_reader(cls, file_path: str) -> FileReader:
        """Create appropriate reader based on file extension"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext not in cls.READERS:
            raise ValueError(f"Unsupported file format: {ext}")
        
        reader_class = cls.READERS[ext]
        return reader_class(file_path)
    
    @classmethod
    def read_file(cls, file_path: str) -> List[Dict[str, Any]]:
        """Convenience method to read a file"""
        reader = cls.create_reader(file_path)
        return reader.read()
