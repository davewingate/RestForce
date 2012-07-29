'''
This module contains functions for authenticting to the force.com platform.

Created on Mar 17, 2012

@author: dwingate
@
'''

from utensils import getUniqueElementValueFromXmlString
from httplib2 import Http, ServerNotFoundError
    
def readLoginCredentialsFromFile(credentialsFilePath):
    with open(credentialsFilePath, 'r') as f:
        username = f.readline().rstrip('\n')
        password = f.readline().rstrip('\n')
        securityToken = f.readline().rstrip('\n')
        return (username, password, securityToken)

def login(username, password, securityToken):
    loginResp, loginRespContent = _callSoapLoginService(username, password, securityToken);

    if loginResp.status != 200:
        raise SalesforceAuthenticationFailedException(loginRespContent)  
    
    return _parseSoapLoginServiceResponse(loginRespContent)  

def _callSoapLoginService(username, password, securityToken):
    '''
    Calls out to the soap login service.
    
    @return: a tuple containing (loginResp, loginRespContent)
    @rtype: a tuple of size 2
    '''
    soapUrl = "https://login.salesforce.com/services/Soap/u/23.0"
    loginSoapRequestBody = """<?xml version="1.0" encoding="utf-8" ?> 
        <env:Envelope 
            xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
            xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
            <env:Body>
                <n1:login xmlns:n1="urn:partner.soap.sforce.com">
                    <n1:username>""" + username + """</n1:username>
                    <n1:password>""" + password + securityToken + """</n1:password>
                </n1:login>
            </env:Body>
        </env:Envelope>"""
    loginSoapRequestHeaders = {
        "content-type":"text/xml",
        "charset":"UTF-8",
        "SOAPAction":"login"
    }
    h = Http()
    try:
        return h.request(soapUrl, "POST", body=loginSoapRequestBody, headers=loginSoapRequestHeaders)   
    except ServerNotFoundError as e:
        raise SalesforceAuthenticationFailedException(e)

def _parseSoapLoginServiceResponse(loginRespContent):
    '''
    Pares the response content from a soap login request, extracting a tuple containing (sessionId, serverUrl, sfInstance).
    
    Example of expected soap login response content:
    <?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="urn:partner.soap.sforce.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <soapenv:Body>
            <loginResponse>
                <result>
                    [...]
                    <serverUrl>https://na10-api.salesforce.com/services/Soap/u/23.0/00DA0000000ZoX3</serverUrl>
                    <sessionId>00DA0000000ZoX3!ARcAQErwnlE.gpvhb82ogWxRVdCfvIQAoaWoZfDSsgUAvp8Xrk0uUHK_wW5us3a3DOX1TCz1V1knqEbXHDaPyY5TxkD1szBO</sessionId>
                    [...]
                </result>
            </loginResponse>
        </soapenv:Body>
    </soapenv:Envelope>
    '''
    sessionId = getUniqueElementValueFromXmlString(loginRespContent, 'sessionId')
    serverUrl = getUniqueElementValueFromXmlString(loginRespContent, 'serverUrl')
    sfInstance = serverUrl.replace('http://', '').replace('https://', '').split('/')[0].replace('-api', '')
    return (sessionId, serverUrl, sfInstance)
    
class SalesforceAuthenticationFailedException(Exception):
    '''
    Thrown to indicate that authentication with Salesforce failed.
    '''
    pass
