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
    def __init__(self, ebo_version="6.0.4.90", server_full_path="/Server 1"):
        self._ebo_version = ebo_version
        self._server_full_path = server_full_path
        self.exported_objects = ET.Element("ExportedObjects") # Placeholder for ExportedObjects
        self.object_set = self._create_object_set()

    @property
    def ebo_version(self):
        return self._ebo_version

    @ebo_version.setter
    def ebo_version(self, value):
        if value != self._ebo_version:
            self._ebo_version = value
            self.object_set = self._create_object_set()

    @property
    def server_full_path(self):
        return self._server_full_path

    @server_full_path.setter
    def server_full_path(self, value):
        if value != self._server_full_path:
            self._server_full_path = value
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
            "Version": self.ebo_version
        })
        self._create_meta_information()
        object_set.append(self.meta_information)
        object_set.append(self.exported_objects)  # Reuse existing ExportedObjects
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
        ET.SubElement(meta_info, "RuntimeVersion", {"Value": self.ebo_version})
        ET.SubElement(meta_info, "SourceVersion", {"Value": self.ebo_version})
        ET.SubElement(meta_info, "ServerFullPath", {"Value": self.server_full_path})
        self.meta_information = meta_info

    def add_to_exported_objects(self, elements):
        """
        Adds elements to the ExportedObjects section of the XML object set.
        Parameters:
            elements (list or Element): A list of XML elements to add.
        """
        if not isinstance(elements, list):
            elements = [elements]
        for e in elements:
            self.exported_objects.append(e)
        # Remove if exists and re-append to end
        if self.exported_objects in self.object_set:
            self.object_set.remove(self.exported_objects)
        self.object_set.append(self.exported_objects)

    def reset_exported_objects(self):
        """
        Resets the ExportedObjects section to an empty <ExportedObjects/> element.
        """
        self.exported_objects = ET.Element("ExportedObjects")
        # Remove the old ExportedObjects and append the new one
        for child in self.object_set.findall("ExportedObjects"):
            self.object_set.remove(child)
        self.object_set.append(self.exported_objects)

    def set_exported_objects(self, elements):
        """
        Creates elements to the ExportedObjects section of the XML object set.
        Replaces any existing children in the ExportedObjects section.
        Parameters:
            elements (list or Element): A list of XML elements to add.
        """
        self.reset_exported_objects()
        self.add_to_exported_objects(elements)

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
    
    def write_xml(self, file_path):
        """
        Writes the pretty-printed XML to the specified file.

        Parameters:
            file_path (str): Path to the output file.
        """
        xml_str = self.to_pretty_xml()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        print(f"XML written to {file_path}")

def to_pretty_xml(obj):
        """
        Converts the XML object to a pretty-printed string.
        Returns:
            str: Pretty-printed XML string.
        """
        rough = ET.tostring(obj, 'utf-8')
        return minidom.parseString(rough).toprettyxml(indent="  ")

def print_pretty_xml(obj):
        """
        Converts the XML object to a pretty-printed string.
        Returns:
            str: Pretty-printed XML string.
        """
        print(to_pretty_xml(obj))