# bidirectional_paper_repository_scripts
This repository contains the scripts and data used to write a paper sent to the MSR 2024 conference.

## Folder Structure

### Scripts


In the folder scripts, we can find the scripts used to extract the results.
* add_year_to_bidir: Organize the bidirectional links by years.
* count_bidir_n_urls: Return the number of bidir urls.
* count_valid_merge_tex: Return the number of merge tex. This file is built in the latex pipeline.
* generate_dataset: This script integrate the results of the PDF pipeline (bidir.json -> evaluation folder) and the Latex pipeline (results_sources_XXX -> evaluation folder). Also, it provides some statistics about the overlap between both pipelines. The result is the dataset described in our paper.
* statistics_bidir: This script returns the distribution of links in the papers. It means, how many papers have 1, 2, 3 links.
* statiscs_raw_bidir: This script returns the distribution of links in all anaThis script download the papers of the category Software Engineering in arxiv.

### corpus

In this folder, you can find the corpus used to evaluate the performance of both pipelines.

### dataset

In this folder, you can find the dataset generated with the bidirectional correspondences between software and paper. It means, a software repository is cited in a paper, and a papers is cited in a software repository.

### evaluation

This folder contains the metrics (precision, recall, f1-score) calculated for both pipelines. You can find them in the files output_metrics_XXXX.json.

Also, you can find the results of the pipelines.
* bidir.json: It is the file with the results of the PDF pipeline. 
* bidir_with_years.json: These are the results of the PDF pipeline distributed by year.
* processed_metadata.json: It contains the results of the analysis of the papers downloaded, including bidir and non bidir papers.
* result_sources_XXXXX.csv: It contains the results of the latex pipeline.

# Requirements

* Python 3.9

# How to use

First, you have to install the python libraries.

pip install -r requirements.txt

THen you can execute each script. Please, note that the folders and name of the files (found in evaluation) can be different, so you will have to change the code to add the correct pathname. 


