import xml.etree.ElementTree as ET

tree = ET.parse('ajaxInputs_random.xml')
root = tree.getroot()
for i,elem in enumerate(root.iter('DOut')):
    print(elem.text)
    
#print(ET.tostring(root))
#tree.write('ajaxInputs_random.xml')