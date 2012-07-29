from distutils.core import setup
import textwrap

setup(
    name='RestForce',
    version='1.0.0',
    author='Dave Wingate',
    author_email='davewingate+restforce@gmail.com',
    packages=['restforce'],
    url='http://pypi.python.org/pypi/RestForce/',
    license='MIT License',
    description='A python API for accessing RESTful resources on the force.com platform.',
    long_description=textwrap.dedent( """\
    
        Usage
        =====

        Rest Force offers a python API for easily working with RESTful resources exposed
        by the `force.com platform <http://www.salesforce.com/platform/>`_. 
        Typical usage often looks like this::
        
            #!/usr/bin/python
            
            from restforce.login import SalesforceAuthenticationFailedException
            from restforce.rest import Resources, RestInvocationException
            
            try:
                r = Resources()
                print r.post('hello', '{ "postData" : "world"}')
                print r.get('hello/1')
                print r.delete('hello/1')
            except SalesforceAuthenticationFailedException as e:
                print e
            except RestInvocationException as e:
                print e
        
        Salesforce REST Example
        =======================
        
        `Creating a REST resource <http://www.salesforce.com/us/developer/docs/apexcode/Content/apex_rest_code_sample_basic.htm>`_ on the force.com platform is easy.  Here's an example:::
        
            @RestResource(urlMapping='/hello/*')
            global class HelloResource {
            
                @HttpGet
                global static String doGet() 
                {
                    return 'Hello, world!';
                }
            
                @HttpDelete
                global static String doDelete() 
                {
                    return 'Good bye, cruel world!';
                }
            
            }

        """),
      classifiers=['Development Status :: 4 - Beta', 'Environment :: Console', 'Intended Audience :: Developers', 'License :: OSI Approved :: MIT License', 'Natural Language :: English', 'Operating System :: OS Independent', 'Topic :: Internet :: WWW/HTTP'],
)