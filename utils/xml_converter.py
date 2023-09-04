from dataclasses import asdict
import re
from dicttoxml import dicttoxml


def to_xml(obj):
    # dict_model = asdict(obj)
    xml = dicttoxml(obj, attr_type=False, root=False).decode('UTF-8')
    all_tags = re.findall('((<.*?>)(.*?)<\/.*?>)', xml)
    for tag in all_tags:
        if re.match('.*item.*', tag[1]):
            continue
        if tag[2] == '':
            tag_name = tag[1][1:-1]
            xml = xml.replace(tag[1], f'<{tag_name} xsi:nil="true">')
    return xml
