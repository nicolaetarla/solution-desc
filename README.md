# Dynamics 365 - Solution Description Generator

This Python script (`solution-desc.py`) is a utility designed to parse a Microsoft Dynamics 365 or Power Apps solution file (`.zip`). It extracts detailed information about the entities, their attributes, and JavaScript web resources contained within the solution and generates a human-readable description.

## Description

The script performs the following actions:
1.  Prompts the user to provide the path to a solution `.zip` file.
2.  Extracts the contents of the zip file into a temporary directory.
3.  Locates the `customizations.xml` file within the extracted contents.
4.  Parses the XML file to retrieve a list of all entities.
5.  For each entity, it lists all its attributes and forms.
6.  The output includes the entity's display name and logical name, as well as each attribute's display name, logical name, and data type.
7.  For each form, the output includes the form's name, description, and type (e.g., main, quick create).
8.  It also locates the `WebResources` folder and lists all the files within it. For each JavaScript file, it parses the content and lists all the declared functions.
9.  The results are printed to the console and saved to a text file named after the original solution file (e.g., `MySolution.txt`).

This provides a quick and easy way to get a high-level overview of the data model customizations and custom code within a solution package.

## Requirements

- Python 3

## Usage

1.  Open a terminal or command prompt.
2.  Navigate to the directory containing the `solution-desc.py` script.
3.  Run the script using the following command:
    ```bash
    python3 solution-desc.py
    ```
4.  When prompted, enter the full path to the solution `.zip` file you want to analyze and press Enter.

    ```
    Enter the path to the solution zip file: /path/to/your/solution.zip
    ```

5.  The script will process the file and display the entity and attribute information on the screen.
6.  A `.txt` file with the same name as your solution zip file (e.g., `solution.txt`) will be created in the same directory with the full output.
