import os
import PyPDF2
import json
import traceback

def read_file(filename):
    if filename.name.endswith(".pdf"):
        try:
            pdfReader = PyPDF2.PdfFileReader(filename)
            text =""
            for page in pdfReader.pages:
                text += page.extractText()
            return text
        except Exception as e:
            raise Exception(f"Error reading the file: {e}")
        
    elif filename.name.endswith(".txt"):
        return filename.read().decode("utf-8")
    
    else:
        raise Exception(f"File type not supported: {filename.name}")    
    
def get_table_data(mcqs):
    table_data = []
    for key,value in mcqs.items():
        mcq = value["mcq"]
        options = " | ".join(
            [
                f"{option}: {option_value}"
                for option, option_value in value["options"].items()
                ]
            )
        correct = value["correct"]
        table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct, "explanations": value["Eplanation"]})

    return table_data