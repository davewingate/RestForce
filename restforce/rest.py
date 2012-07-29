'''
Main module for interacting with RESTful resources on the force.com platform.

Created on Apr 4, 2012

@author: dwingate
'''

from os.path import expanduser
from httplib2 import Http, MalformedHeader, ServerNotFoundError
from restforce.login import login, readLoginCredentialsFromFile

class Resources(object):
    '''
    Represents the RESTful resources exposed to a single force.com user session.
    '''

    def __init__(self, credentialsFileOrUserName=expanduser('~/.restforce'), password=None, securityToken=None):
        '''
        Creates a Resources object associated with a single Salesforce session.
        
        Authentication credentials can be explicitly provided to the method:
            new Resources('user@domain.com', 'secret_password', 'security_token')
            
        Alternatively, credentials can be extracted from a file on the file system:
            new Resources('/path/to/credentials/file')
        where /path/to/credentials/file contains:
            user@domain.com
            secret_password
            security_token
            
        Or, more succinctly, credentials can be extracted by convention from the .restforce
        file in your home directory:
            new Resources()
        
        @raise SalesforceAuthenticationFailedException: if user cannot be authenticated using credentials provided.
        '''
        if password != None and securityToken != None:
            username = credentialsFileOrUserName
            (self.sessionId, self.serverUrl, self.sfInstance) = login(username, password, securityToken)
        else:
            credentialsFilePath = credentialsFileOrUserName
            credentialsFromFile = readLoginCredentialsFromFile(credentialsFilePath)
            (self.sessionId, self.serverUrl, self.sfInstance) = login(credentialsFromFile[0], credentialsFromFile[1], credentialsFromFile[2])
            
    def getSessionId(self):
        '''
        Returns the force.com sessionId associated with this Resources object.
        '''
        return self.sessionId
    
    def getSfInstance(self):
        '''
        Returns the force.com server instance associated with this Resources object.
        '''
        return self.sfInstance
    
    def get(self, resourceName):
        '''
        Executes an HTTP GET request for the named resource.
        '''
        return self._callRestMethod('GET', resourceName)
    
    def delete(self, resourceName):
        '''
        Executes an HTTP DELETE request against the named resource.
        '''
        return self._callRestMethod('DELETE', resourceName)
    
    def put(self, resourceName, jsonDataString):
        '''
        Executes an HTTP PUT request on the named resource.
        '''
        return self._callRestMethod('PUT', resourceName, jsonDataString)
    
    def post(self, resourceName, jsonDataString):
        '''
        Executes an HTTP POST request to the named resource.
        '''
        return self._callRestMethod('POST', resourceName, jsonDataString)
            
    def _callRestMethod(self, httpMethod, resourceName, jsonDataString="{}"):
        """
        Invokes a REST method on a salesforce resoruce, optionally passing a data paylod.
        If REST invocation fails, a RestInvocationException is raised.
        """
        restRequestHeaders = {
            "content-type":"application/json", 
            "Authorization":"OAuth " + self.sessionId, 
            "X-PrettyPrint":"1"
        }
        httpResource = "https://" + self.sfInstance + "/services/apexrest/" + resourceName
        h = Http()
        try:
            restResponse, restContent = h.request(httpResource, httpMethod, body=jsonDataString, headers=restRequestHeaders)
            if restResponse.status < 200 or restResponse.status > 299:
                raise RestInvocationException('Status ' + str(restResponse.status) + ': ' + restContent)
            return restContent
        except MalformedHeader:
            raise RestInvocationException('Invalid sessionId')
        except ServerNotFoundError as e:
            raise RestInvocationException(e)
        
class RestInvocationException(Exception):
    '''
    Thrown to indicate that invocation of REST method resulted in a non-successful response code.
    '''
    pass