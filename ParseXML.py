import xml.etree.ElementTree as ET 
import requests

def resolve_properties(root):
    try:
        properties = {}
        ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}

        for prop in root.findall(".//maven:properties/*", ns):
            prop_name = prop.tag.split('}')[1]
            properties[prop_name] = prop.text 

        return properties
    except Exception as e:
        print(f'Error while resolving properties: {e}')

def parse_dependencies(url):
    response = requests.get(url)
    
    try:
        if response.status_code == 200:
            # print(f"Successfully fetched the pom URL: {url}")
            content = response.text
            # print(content)
            root = ET.fromstring(content)
            
            dependencies = {}
            properties = resolve_properties(root)
            # print(properties)

            ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}
            for dependency in root.findall(".//maven:dependencyManagement/maven:dependencies/maven:dependency", ns):
                groupId = dependency.find("maven:groupId", ns).text
                artifactId = dependency.find("maven:artifactId", ns).text
                
                version_element = dependency.find("maven:version", ns)
                version = version_element.text if version_element is not None else None

                if version and version.startswith("${") and version.endswith("}"):
                    prop_name = version[2:-1] 
                    version = properties.get(prop_name, version)

                key = f"{groupId}:{artifactId}"

                dependencies[key] = {"groupId": groupId, "artifactId": artifactId, "version": version}

            return dependencies
        else:
            print(f"Failed to fetch the URL. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f'Error while parsing pom.xml: {e}') 
