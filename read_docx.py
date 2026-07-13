import zipfile
import xml.etree.ElementTree as ET
import sys

def read_docx(file_path):
    try:
        with zipfile.ZipFile(file_path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            text = []
            for t in tree.findall('.//w:t', namespaces):
                if t.text:
                    text.append(t.text)
            return '\n'.join(text)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    print(read_docx(sys.argv[1]))
