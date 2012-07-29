'''
Created on Mar 17, 2012

@author: dwingate
'''
import unittest
from restforce.utensils import getUniqueElementValueFromXmlString


class Test(unittest.TestCase):
        
    def testGetUniqueElementValueFromXmlString_NoSuchElement(self):
        xmlString = '<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>'
        value = getUniqueElementValueFromXmlString(xmlString, 'no_such_element')
        self.assertIsNone(value)
        
    def testGetUniqueElementValueFromXmlString_OneMatchingElement(self):
        xmlString = '<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>'
        value = getUniqueElementValueFromXmlString(xmlString, 'foo')
        self.assertEqual('bar', value)

    def testGetUniqueElementValueFromXmlString_MultipleMatchingElements(self):
        xmlString = '<?xml version="1.0" encoding="UTF-8"?><foos><foo>biz</foo><foo>baz</foo><foo>bar</foo></foos>'
        value = getUniqueElementValueFromXmlString(xmlString, 'foo')
        self.assertEqual('biz', value)


if __name__ == "__main__":
    unittest.main()