'''
This is a functional test that has some external preconditions:
 - a valid ~/.restforce credentials file
 - a RESTful Apex resource named 'hello' ... something like:
 
        @RestResource(urlMapping='/hello/*')
        global class HelloResource {

            @HttpGet
            global static String doGet() { return 'Hello, GET!'; }
        
            @HttpDelete
            global static String doDelete() { return 'Hello, DELETE!'; }
        
            @HttpPost
            global static String doPost(String postData) { return 'Hello, POST! ... ' + postData; }
        
            @HttpPut
            global static String doPut(String putData) { return 'Hello, PUT! ... ' + putData; }

        }

Created on Mar 18, 2012

@author: dwingate
'''
import unittest
from os.path import expanduser
from restforce.login import readLoginCredentialsFromFile
from restforce.rest import Resources

class Test(unittest.TestCase):

    def testInit(self):
        r1 = Resources()
        self.assertIsNotNone(r1.getSessionId())
        self.assertIsNotNone(r1.getSfInstance())
        
        r2 = Resources(expanduser('~/.restforce'))
        self.assertEquals(r1.getSessionId(), r2.getSessionId())
        self.assertEquals(r1.getSfInstance(), r2.getSfInstance())
        
        credentials = readLoginCredentialsFromFile(expanduser('~/.restforce'))
        r3 = Resources(credentials[0], credentials[1], credentials[2])
        self.assertEquals(r2.getSessionId(), r3.getSessionId())
        self.assertEquals(r2.getSfInstance(), r3.getSfInstance())
    
    def testPost(self):
        r = Resources()
        print r.post('hello', '{ "postData": "post post post" }')
        
    def testGet(self):
        r = Resources()
        print r.get('hello/1')
    
    def testPut(self):
        r = Resources()
        print r.put('hello/1', '{ "putData": "put put put" }')
        
    def testDelete(self):
        r = Resources()
        print r.delete('hello/1')

if __name__ == "__main__":
    unittest.main()