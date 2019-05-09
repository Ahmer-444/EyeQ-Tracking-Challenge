import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET

from time import sleep
'''
This python utility converts images and annotations to xml files
'''

def write_xml(folder, image, filename, path, objects, bbox, savedir):
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    height, width, depth = image.shape

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = folder
    ET.SubElement(annotation, 'filename').text = filename
    ET.SubElement(annotation, 'path').text = path
    

    source = ET.SubElement(annotation, 'source')
    ET.SubElement(source, 'database').text = 'Unknown'

    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)

    ET.SubElement(annotation, 'segmented').text = '0'

    for (xmin,ymin,xmax,ymax),obj in zip(bbox,objects):
        
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = obj
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bndbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(xmin)
        ET.SubElement(bndbox, 'ymin').text = str(ymin)
        ET.SubElement(bndbox, 'xmax').text = str(xmax)
        ET.SubElement(bndbox, 'ymax').text = str(ymax)

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    save_path = os.path.join(savedir, filename.replace('jpg', 'xml'))
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)
    cv2.imwrite(os.path.join(folder, filename),image)


if __name__ == '__main__':
    """
    for testing
    """

    folder = 'data'
    path = os.path.abspath(folder)
    objects = 'swimmer'
    bbox = [(587,530,617,549),(587,530,617,549)]
    savedir = 'annotations'

    for filename in os.listdir(folder):
        write_xml(folder, filename, path, objects, bbox, savedir)
        break
    


