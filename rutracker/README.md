Introduction
============
This folder contains functional tests for rutracker API v1 [1].

These tests were designed as an example of the functional tests
for REST API services.

All tests were created in 1-2 days and can be improved, of course.

[1] http://api.rutracker.org/v1/docs/

How To Run Tests
================

To run sanity suite execute:

  py.test -v -m 'sanity'

To run negative test suite:

  py.test -v -m 'negative'

To run long tests:

  py.test -v -m 'long'
