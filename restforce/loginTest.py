'''
Created on Mar 17, 2012

@author: dwingate
'''
import unittest
from os.path import expanduser
from restforce.login import login, readLoginCredentialsFromFile, \
    SalesforceAuthenticationFailedException, \
    _callSoapLoginService, _parseSoapLoginServiceResponse


class Test(unittest.TestCase):

    def testReadLoginCredentialsFromFile(self):
        (username, password, securityToken) = readLoginCredentialsFromFile(expanduser('~/.restforce'))
        self.assertIsNotNone(username, "Check your ~/.restforce file?")
        self.assertIsNotNone(password, "Check your ~/.restforce file?")
        self.assertIsNotNone(securityToken, "Check your ~/.restforce file?")

    def testLogin(self):
        self.assertRaises(SalesforceAuthenticationFailedException, login, 'unknown user name', 'password', 'security token')

    def testCallSoapLoginService(self):
        loginResp = _callSoapLoginService('unknown user name', 'password', 'security token')
        self.assertGreaterEqual(loginResp, 400)
        
    def testParseSoapLoginServiceResponse(self):
        loginResponseContent = '''<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="urn:partner.soap.sforce.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <soapenv:Body>
                <loginResponse>
                    <result>
                        <serverUrl>https://na10-api.salesforce.com/services/Soap/u/23.0/00DA0000000ZoX3</serverUrl>
                        <sessionId>fooBarBaz</sessionId>
                    </result>
                </loginResponse>
            </soapenv:Body>
        </soapenv:Envelope>
        '''
        sessionid, serverUrl, sfInstance = _parseSoapLoginServiceResponse(loginResponseContent)
        self.assertEqual(sessionid, 'fooBarBaz');
        self.assertEqual(serverUrl, 'https://na10-api.salesforce.com/services/Soap/u/23.0/00DA0000000ZoX3');
        self.assertEqual(sfInstance, 'na10.salesforce.com');
        
        

if __name__ == "__main__":
    unittest.main()