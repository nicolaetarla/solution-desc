import xml.etree.ElementTree as ET
import sys
import zipfile
import os
import shutil

def parse_customizations(xml_file, output_file):
    """
    Parses the customizations.xml file and extracts the names of all entities.

    Args:
        xml_file (str): The path to the customizations.xml file.
        output_file: File handle to write the output to.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find all Entity tags and print the text of their Name tag
    for entity in root.findall('.//Entity'):
        name_tag = entity.find('Name')
        if name_tag is not None:
            entity_name = name_tag.text
            localized_name = name_tag.get('LocalizedName')
            if not localized_name:
                localized_name = entity_name
            
            line = f"Entity: {localized_name} [{entity_name}]"
            print(line)
            output_file.write(line + '\n')

            attributes = entity.findall('.//attribute')
            if attributes:
                line = "  Fields:"
                print(line)
                output_file.write(line + '\n')
                for attribute in attributes:
                    name_tag = attribute.find('Name')
                    type_tag = attribute.find('Type')
                    displayname_tag = attribute.find('displaynames/displayname')

                    if name_tag is not None and name_tag.text is not None and type_tag is not None and type_tag.text is not None:
                        name = name_tag.text
                        type = type_tag.text
                        display_name = name
                        if displayname_tag is not None:
                            description = displayname_tag.get('description')
                            if description:
                                display_name = description
                        
                        line = f"    - {display_name} [{name}] ({type})"
                        print(line)
                        output_file.write(line + '\n')

            forms_tags = entity.findall('FormXml/forms')
            if forms_tags:
                has_systemforms = any(ft.find('systemform') is not None for ft in forms_tags)
                if has_systemforms:
                    line = "  Forms:"
                    print(line)
                    output_file.write(line + '\n')

                for forms_tag in forms_tags:
                    form_type = forms_tag.get('type')
                    for systemform in forms_tag.findall('systemform'):
                        # Correctly navigate to the LocalizedName and Description tags
                        form_name_tag = systemform.find('LocalizedNames/LocalizedName')
                        description_tag = systemform.find('Descriptions/Description')

                        form_name = form_name_tag.get('description') if form_name_tag is not None else "N/A"
                        description = description_tag.get('description') if description_tag is not None else ""
                        if not description:
                            description = "[no description]"

                        if form_name != "N/A":
                            line = f"    - {form_name} - {description} ({form_type})"
                            print(line)
                            output_file.write(line + '\n')


def find_customizations_xml(directory):
    """
    Finds the customizations.xml file in a directory.
    """
    for root, dirs, files in os.walk(directory):
        if "customizations.xml" in files:
            return os.path.join(root, "customizations.xml")
    return None

def main():
    zip_file_path = input("Enter the path to the solution zip file: ")

    if not os.path.exists(zip_file_path):
        print(f"Error: File not found at {zip_file_path}")
        sys.exit(1)
    
    if not zipfile.is_zipfile(zip_file_path):
        print(f"Error: {zip_file_path} is not a valid zip file.")
        sys.exit(1)

    output_filename = os.path.splitext(os.path.basename(zip_file_path))[0] + ".txt"
    extract_dir = "temp_extracted_solution"
    
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
        
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
        customizations_xml_path = find_customizations_xml(extract_dir)
        
        if customizations_xml_path:
            with open(output_filename, 'w') as output_file:
                parse_customizations(customizations_xml_path, output_file)
            print(f"\nOutput also written to {output_filename}")
        else:
            print("Error: customizations.xml not found in the zip file.")
            
        shutil.rmtree(extract_dir)


if __name__ == "__main__":
    main()