## General Introduction

This script was written as a showcase on how to embed pySROS into a GitLab CICD pipeline. The use-case shown here is a simple MD-SROS config retrieval and transformation into JSON format. 

## Elements and SW Versions tested with

| Element                | Version                                      |
|------------------------|----------------------------------------------|
|   GitLab Version       |    15.4.6                                    |
|   Dev Python Version   |    Python 3.10.12                            |
|   SROS Versions        |    22.5R1 to 23.7R2                          |

## Components

This repo consists of 3 main components:
- gitlab-ci.yaml
- backup.py
- inventory.py

The gitlab-ci.yaml is the pipeline definition to be used in a GitLab repository.
The inventory.py script handles the repo's directory structure.
The backup.py script uses the pySROS library to pull the NEs configuration and to transform it into JSON format. 

## Usage Description

The pipeline consists of two stages each running a single job:

1. inventory

In the inventory stage a single job is being executed based on the inventory.py script. It reads the inventory.yaml file and based on the specified network elements a dedicated directory for each network element is created. 

2. backup

In the backup stage a single job is being executed based on the backup.py script. The script reads the inventory.yaml file and loops through it. For each specified network element is connects via NetConf, pulls the config and writes it into a file in case there was a change compared to the previous one. 

In the pipeline definition itself the subsequent git add, commit, push is being handled to allow pushing config changes back into the repo itself. 

## Other Notes

- The NEs credentials can be stored in GitLab CI/CD Settings as variables. The backup.py script is written to pull the variables using os.getenv() function. 