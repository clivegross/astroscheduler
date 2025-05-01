import xml.etree.ElementTree as ET
from xml.dom import minidom


class EBOXMLBuilder:
    """
    A class to build an EBO XML structure for importing objects. Creates an XML object ready for EBO import.
    Add objects to the ExportedObjects section using the add_to_exported_objects method.
        <?xml version="1.0" ?>
        <ObjectSet ExportMode="Standard" Note="TypesFirst" SemanticsFilter="Standard" Version="6.0.4.90">
        <MetaInformation>
            <ExportMode Value="Standard"/>
            <SemanticsFilter Value="None"/>
            <RuntimeVersion Value="6.0.4.90"/>
            <SourceVersion Value="6.0.4.90"/>
            <ServerFullPath Value="/Server 1"/>
        </MetaInformation>
        <ExportedObjects/>
        </ObjectSet>
    """
    def __init__(self, version="6.0.4.90", server_full_path="/Server 1"):
        self.version = version
        self.server_full_path = server_full_path
        self.object_set = self._create_object_set()

    def _create_object_set(self):
        """
        Creates the root ObjectSet element of the XML structure.
        Returns:
            Element: The root ObjectSet element.
        """
        object_set = ET.Element("ObjectSet", {
            "ExportMode": "Standard",
            "Note": "TypesFirst",
            "SemanticsFilter": "Standard",
            "Version": self.version
        })
        meta_info = self._create_meta_information()
        object_set.append(meta_info)
        ET.SubElement(object_set, "ExportedObjects")
        return object_set

    def _create_meta_information(self):
        """
        Creates the MetaInformation section of the XML object set.
        Returns:
            Element: The MetaInformation element.
        """
        meta_info = ET.Element("MetaInformation")
        ET.SubElement(meta_info, "ExportMode", {"Value": "Standard"})
        ET.SubElement(meta_info, "SemanticsFilter", {"Value": "None"})
        ET.SubElement(meta_info, "RuntimeVersion", {"Value": self.version})
        ET.SubElement(meta_info, "SourceVersion", {"Value": self.version})
        ET.SubElement(meta_info, "ServerFullPath", {"Value": self.server_full_path})
        return meta_info

    def add_to_exported_objects(self, elements):
        """
        Adds elements to the ExportedObjects section of the XML object set.
        Parameters:
            elements (list or Element): A list of XML elements to add.
        """
        if not isinstance(elements, list):
            elements = [elements]
        exported = self.object_set.find("ExportedObjects")
        for e in elements:
            exported.append(e)

    def to_pretty_xml(self):
        """
        Converts the XML object to a pretty-printed string.
        Returns:
            str: Pretty-printed XML string.
        """
        rough = ET.tostring(self.object_set, 'utf-8')
        return minidom.parseString(rough).toprettyxml(indent="  ")

    def get_object_set(self):
        """
        Returns the XML object set.
        Returns:
            Element: The root element of the XML object set.
        """
        return self.object_set
    
    def write_pretty_xml(self, file_path):
        """
        Writes the pretty-printed XML to the specified file.

        Parameters:
            file_path (str): Path to the output file.
        """
        xml_str = self.to_pretty_xml()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)