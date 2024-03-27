import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def create_xml_variable(variable_name, data_type, address):
    variable = ET.Element("variable")
    variable.set("name", variable_name)
    
    type_element = ET.SubElement(variable, "type")
    if data_type == "Bool":
        ET.SubElement(type_element, "BOOL")
    elif data_type == "Int":
        ET.SubElement(type_element, "INT")
    elif data_type == "Real":
        ET.SubElement(type_element, "REAL")
    
    initial_value = ET.SubElement(variable, "initialValue")
    if data_type == "Bool":
        ET.SubElement(initial_value, "simpleValue", value="False")
    else:
        ET.SubElement(initial_value, "simpleValue", value="0")
    
    variable.set("address", address)
    
    return variable

def generate_address(text):
    if "Input Reg " in text:
        num = int(text.replace("Input Reg ", "").strip()) + 100
        new_address = f"%IW{num}"
    elif "Holding Reg " in text:
        num = int(text.replace("Holding Reg ", "").strip()) + 100
        new_address = f"%QW{num}"
    elif "Input " in text:
        num = text.replace("Input ", "").strip()
        new_address = f"%IX100.{num}"
    elif "Coil " in text:
        num = text.replace("Coil ", "").strip()
        new_address = f"%QX100.{num}"
    else:
        new_address = "Invalid Address"
    
    return new_address

# Definir la estructura XML
root = ET.Element("globalVars")

# Abrir el archivo CSV y leer sus contenidos con encoding UTF-8
with open('archivo.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Limpiar el nombre de la variable si hay caracteres no deseados
        variable_name = list(row.values())[0].replace("  "," ").replace(" ","_").replace("-","_").replace("(","").replace(")","").replace("&","and")

        data_type = row["Data Type"]
        address = generate_address(row["Address"])
        
        variable = create_xml_variable(variable_name, data_type, address)
        root.append(variable)

# Crear el árbol XML
tree = ET.ElementTree(root)

# Formatear el XML
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

# Escribir el XML en un archivo
with open("variables.xml", "w", encoding="utf-8") as xml_file:
    xml_file.write(xmlstr)
