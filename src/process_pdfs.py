import os
from azureml.core import Run, Dataset
import configparser
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient, AnalyzeResult
from azure.core.serialization import AzureJSONEncoder
import json

def process_pdfs(input_dir, output_dir, doc_endpoint, doc_key, model_id):
    # Initialize the DocumentAnalysisClient
    document_analysis_client = DocumentAnalysisClient(
        endpoint=doc_endpoint, credential=AzureKeyCredential(doc_key)
    )

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each PDF file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")

            with open(input_path, 'rb') as form:
                poller = document_analysis_client.begin_analyze_document(model_id, form)
                result = poller.result()

            # Convert result to dictionary and save as JSON
            result_dict = result.to_dict()
            with open(output_path, 'w') as f:
                json.dump(result_dict, f, cls=AzureJSONEncoder)

            print(f"Processed {filename} and saved result to {output_path}")

# The input and output directories, endpoint, key, and model ID are provided as command-line arguments
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True)
    parser.add_argument('--output_dir', type=str, required=True)
    parser.add_argument('--doc_endpoint', type=str, required=True)
    parser.add_argument('--doc_key', type=str, required=True)
    parser.add_argument('--model_id', type=str, default="citi_test_model")
    args = parser.parse_args()

    process_pdfs(args.input_dir, args.output_dir, args.doc_endpoint, args.doc_key, args.model_id)