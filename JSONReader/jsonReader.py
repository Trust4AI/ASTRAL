# -*- coding: utf-8 -*-

import os
import json

class JSONReader:
    
    def read_from_json(dataset_path, dataset_name):
        # Get the directory path of the Flask application
        base_dir = os.path.dirname(os.path.abspath(dataset_path))

        # Path to the folder containing the dataset
        data_folder = os.path.join(base_dir, dataset_path)

        # Path to the dataset JSON file
        dataset_file = os.path.join(data_folder, dataset_name)

        # Load the JSON dataset
        with open(dataset_file, 'r') as f:
            dataset = json.load(f)       
            
        return dataset
