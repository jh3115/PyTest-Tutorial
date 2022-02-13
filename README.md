# PyTest-Tutorial
A Pytest walk through covering a simple use case, marks, custom marks, fixtures and my favourite plugins. 
## Pycon - Ireland
### PyTest Tutorial 9 Feb 2022

### Overview
Pytest is an external python library that makes testing your code very easy. It has a clean syntax
that doesn't rely on the class approach used by _unittest_ and instead uses a straight forward _assert_. 
In it's simplest cases you don't even need to import pytest into your test file. 
Don't let that fool you though as pytest is a powerful tool that will have you writing easily understood, 
clean and useful unittests to test your code. 
### Marking
https://docs.pytest.org/en/6.2.x/reference.html#marks    
Marks allow us to add metadata to test functions but not to fixtures. However, this metadata can then be used by plugins 
and fixtures. 
```python
import pytest

@pytest.mark.my_mark
def test_foo():
    assert foo() == 'foo'
``` 
Although this works straight from the box be sure to register your custom markers in your pytest.ini file like so:
```
# contents of pytest.ini
[pytest]
markers =
    my_mark: mark test as a my_mark test.
```
You can then run your marked test using
```
$ pytest -m my_mark
```
### Fixtures

https://docs.pytest.org/en/6.2.x/reference.html#fixtures   
Fixtures are essentially context managers that allow us to effectively manage resources 
during testing. As your app gets larger you'll probably start incorporating other web services,
or databases into your code. It's really bad practice for you to actually reach out to these
services during oyour test framework so fixtures allows you to essentially fake the service you
require and allows you to work around it. At RenRe as I mentioned we heavily use the AWS suite of 
services and so I'll show you how we could possibly use a mocked s3 client.
An important thing about fixtures also is the scope of each fixture. Mostly the innitialisation of
such a service could be costly if you had to do it for every function, which is an option available
but instead it's usually sufficient to instatiate your fixture in the scope of a module. 
Let me show you what I mean with an example 

### Plugins

Three of my favourite plugins so far are:    
- **pytest-sugar:** this is effectively a UI improvement, which makes the report nicer to read.    
- **pytest-cov:** a great tool to measure how well excercised your code is. It is a great tool as it auto-generates 
a report for you and automatically collates all your coverage reports. You can also specify if you want the report 
to generate a html version of the report for you,, making it super easy to read.    
- **pytest-repeat:** TODO
