import pytest


def get_test_case_docstring(item):
    """ This function gets doc string from test case and format it
        to show this docstring instead of the test case name in reports.
    """

    param_str = 'long string ({0} characters) started from "{1}"'

    if item._obj.__doc__:

        # Determine the name of component (Note: the name of directory
        # inside the root of test repository should be equal to the name
        # of the component):
        previous = ''
        for name in str(item.fspath).split('/'):
            if previous == 'component_tests':
                full_name = name.upper() + ' | '
            previous = name

        # Remove extra whitespaces from the doc string:
        name = item._obj.__doc__.strip()
        full_name += ' '.join(name.split())

        # Generate the list of parameters for parametrized test cases:
        if hasattr(item, 'callspec'):
            params = item.callspec.params

            if params:
                for key in params:
                    param = str(params[key])
                    param_len = len(param)

                    # If value of some parameter is too long to show it in
                    # reports we should replace this value with some default
                    # string to make sure the report will looks good:
                    if param_len > 50:
                        params[key] = param_str.format(param_len, param[:10])

            # Add dict with all parameters to the name of test case:
            full_name += ' Parameters: ' + str(params)

    return full_name


def pytest_itemcollected(item):
    """ This function modifies names of test cases "on the fly"
        during the execution of test cases.
    """

    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)


def pytest_collection_finish(session):
    """ This function modified names of test cases "on the fly"
        when we are using --collect-only parameter for pytest
        (to get the full list of all existing test cases).
    """

    if session.config.option.collectonly is True:
        for item in session.items:
            # If test case has a doc string we need to modify it's name to
            # it's doc string to show human-readable reports and to
            # automatically import test cases to test management system.
            if item._obj.__doc__:
                full_name = get_test_case_docstring(item)
                print full_name

    pytest.exit('Done!')
