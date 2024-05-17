from azureml.core import Dataset, Run
import os
import shutil

def update_or_create_pdf_dataset(output_dir):
    run = Run.get_context()
    ws = run.experiment.workspace
    
    datastore = ws.datastores['input_pdfs']
    path_on_datastore = (datastore, '**/*.pdf')
    
    # Create or update dataset
    pdf_dataset = Dataset.File.from_files(path=path_on_datastore)
    pdf_dataset.register(workspace=ws, name='PDF File Dataset',
                         description='Dataset containing all PDF files from the input_pdfs datastore',
                         create_new_version=True)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Download files to the output directory
    pdf_files = pdf_dataset.download(target_path=output_dir, overwrite=True)

    print("Dataset updated or created successfully and files saved to output directory.")

# The output directory is provided as a command-line argument
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str, required=True)
    args = parser.parse_args()

    update_or_create_pdf_dataset(args.output_dir)