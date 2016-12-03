import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus
import schema

from collections import defaultdict

# Global Constants

# File paths to read and write the data
OSM_FILE = "full_map.osm"
OSM_PATH = "data/" + OSM_FILE
CLEAN_PATH = "processed_data/"

OSM_CLEANED_PATH = CLEAN_PATH + "cleaned_" + OSM_FILE
NODES_PATH = CLEAN_PATH + "nodes.csv"
NODE_TAGS_PATH = CLEAN_PATH + "nodes_tags.csv"
WAYS_PATH = CLEAN_PATH + "ways.csv"
WAY_NODES_PATH = CLEAN_PATH + "ways_nodes.csv"
WAY_TAGS_PATH = CLEAN_PATH + "ways_tags.csv"

# Schema for validation
SCHEMA = schema.schema

# Fields for the different types of elelments
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version',
                'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# REGEX for the identifying charicters that will cause issues
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# Helper functions to clean up the data
def hasNumbers(inputString):
    '''Check if there is a number in string'''
    return any(char.isdigit() for char in inputString)

def is_street_name(elem):
    '''Check if element is a street name'''
    return (elem.attrib['k'] == "addr:street")

def update_name(name, mapping):
    '''Convert abbreviations to a preferred name'''
    road_type = name.split()[-1:][0]
    cleaned = mapping[road_type]
    name = name.replace(road_type, cleaned)
    return name

def add_alt_name(elem, alt_name, element_id, tag_list):
    '''Add a new tag for alternate names'''
    type_key = k_prep(elem)
    tag_type = type_key[0]
    tag_list.append({'id': element_id,
            'key': 'alt_name',
            'value': alt_name,
            'type': tag_type})

def k_prep(elem):
    '''Convert k attributes to tag_type and tag_key'''
    k = elem.attrib['k'].split(':', 1)

    if len(k) > 1:
        tag_type = k[0]
        tag_key = k[1]
    else:
        tag_type = 'regular'
        tag_key = k[0]

    return (tag_type, tag_key)

def value_cleaner(elem, tag_key, tag_type, element_id, tag_list):
    '''Clean various issues with v attributes'''
    value = elem.attrib['v']
    if is_street_name(elem) and value.split()[-1:][0] not in expected:
        try:
            value = update_name(value, mapping)
        except:
            print "No suggestion for:" + value

    # Some alternate names are included as ; seperated list this moves them
    # to an alt_name tag instead.
    elif tag_key == 'name' and ';' in value and tag_type != 'flag':
        values = value.split(';')
        value = values[0]
        add_alt_name(elem, values[1], element_id, tag_list)

    # Tricky to sort out abreviations, phone numbers, zips, etc. this catches
    # most issues of all capital phrases.
    if value == value.upper() and ' ' in value:
        if hasNumbers(value) == False:
            value = value.title()

    return value

# Types of roadways we expect to see
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Pike",
            "Highway", "Way"]

# Fixing roadway issues seen in this dataset
mapping = { "Blvd." : "Boulevard", #
            "Ct" : "Court",
            "Dr" : "Drive",
            "St" : "Street",
            "St." : "Street",
            "ST" : "Street", #
            "Ave" : "Avenue",
            "Ave." : "Avenue", #
            "Rd." : "Road",
            "Rd" : "Road"
            }

def shape_element(element, node_attr_fields=NODE_FIELDS,
                    way_attr_fields=WAY_FIELDS, problem_chars=PROBLEMCHARS,
                    default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []

    nd_count = 0
    for elem in element.iter():
        element_id = element.attrib['id']

        if elem.tag == 'nd':
            way_nodes.append({'id' : element_id,
                                'node_id': elem.attrib['ref'],
                                'position': nd_count})
            nd_count += 1
        elif elem.tag == 'tag':
            # skip to next iteration if their are problem characters
            if re.search(problem_chars, elem.attrib['k']):
                continue

            type_key = k_prep(elem)
            tag_type = type_key[0]
            tag_key = type_key[1]

            value = value_cleaner(elem, tag_key, tag_type, element_id, tags)

            tags.append({'id': element_id,
                        'key': tag_key,
                        'value': value,
                        'type': tag_type})

    if element.tag == 'node':
        node_attribs = {x : element.attrib[x] for x in node_attr_fields }
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        way_attribs = {x : element.attrib[x] for x in way_attr_fields }
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
#         Shamelessly borrowed from class            #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


# Run everything we have set up above
process_map(OSM_PATH, True)
