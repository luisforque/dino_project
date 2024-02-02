![image](https://github.com/luisforque/dino_project/assets/1584297/4abe93e2-0291-456c-bab7-c8b61682a611)

## Source Data

https://www.nhm.ac.uk/discover/dino-directory.html

## Goal and Success Criteria

The goal is to have a clean relational database with all the information on dinousaurs, while validating knowledge and gathering skills.

The success criteria is being able to collect information from a RDBMS locally and present it on a python simple dashboard.

Main questions to answer:

- Is there a correlation between era and size?

## Steps

- Create an architectural diagram for the solution
- Use Python and webscraping to collect all the Dinosaur data from the National History Museum
- Store the body content locally in a file server (emulating a backup)
- Store the relevant information as a json file in the file server (emulating a data lake)
- Create a ERM for the database considering the information available
- Create a SQL script to create the database and the tables
- Use the files stored locally to transform the data using Python
- Load the (normalized) data into a local RDBMS (MySQL) using Python
- Using Python and Jupyter Notebook, present relevant information

## Results

Architectural diagram: https://lucid.app/lucidchart/fb334a4e-4a8f-43e5-a71b-6b1ab6d75f65/edit?viewport_loc=-262%2C-400%2C3600%2C1719%2C0_0&invitationId=inv_1f027161-2ae0-4dd7-afc1-22819036381b

Data modelling: https://dbdiagram.io/d/65b93d64ac844320ae10e75c

![data_model.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/00b9e1cd-6bbc-45d4-b7f9-3e713b6998bc/617d619d-8137-45f6-b823-a54e94bad0cc/data_model.png)

##Data collected
![image](https://github.com/luisforque/dino_project/assets/1584297/44d87868-c156-4ed8-893f-62a8d862353e)
NMost Dinosaurs species were discovered recently

![image](https://github.com/luisforque/dino_project/assets/1584297/572fcd8b-ddcc-4cb2-a616-4ffe7b550361)
Most Dinosaurs species are smaller than 6 meters.

![image](https://github.com/luisforque/dino_project/assets/1584297/34e8f912-9275-4b27-941e-2b214ff5bd07)
Most Dinosaur species were herbivorous.

![image](https://github.com/luisforque/dino_project/assets/1584297/24fa68af-eae6-450c-ac1e-31267d002c56)
While there were smaller Dinosaur species throughout, the larger ones are only seen in more recent times (150 million years back or less)

## Known Issues

- There are some limitations on the data collected, some Dinosaurs without size and/or year on which it was named.
- The countries are not correctly parsed when there are more than one country found for a Dino species.
- Dinosaur names with a - on the name are not immediately found on the data source.
- Description is a column with 1000 chars on the database, and if the description is larger than that, the field is being cropped.
