import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def create_xml_variable(variable_name, data_type):
    variable = ET.Element("variable")
    variable.set("name", variable_name)
    
    type_element = ET.SubElement(variable, "type")
    if data_type == "Bool":
        ET.SubElement(type_element, "BOOL")
    elif data_type == "Int":
        ET.SubElement(type_element, "INT")
    elif data_type == "Real":
        ET.SubElement(type_element, "REAL")
        
    return variable

# Definir la estructura XML
root = ET.Element("externalVars")

# Abrir el archivo CSV y leer sus contenidos con encoding UTF-8
with open('archivo.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Limpiar el nombre de la variable si hay caracteres no deseados
        variable_name = list(row.values())[0].replace("  "," ").replace(" ","_").replace("-","_").replace("(","").replace(")","").replace("&","and")

        data_type = row["Data Type"]
        
        
        variable = create_xml_variable(variable_name, data_type)
        root.append(variable)

# Crear el árbol XML
tree = ET.ElementTree(root)

# Formatear el XML
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

# Escribir el XML en un archivo
with open("variablesExt.xml", "w", encoding="utf-8") as xml_file:
    xml_file.write(xmlstr)
