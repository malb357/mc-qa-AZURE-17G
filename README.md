# mc-qa-azure-17G

The aim of this project is create a set of automatic functional tests for the the New Azure Experience sku 17G.
The test cases are developed in Python wrapper tool Toolium using Behave. 

What is Behave?
It's a behavior-driven development (BDD), Python style. For more detail about BDD check https://behave.readthedocs.io/en/latest/philosophy.html

----


Getting Started
---------------
This project was started from `Toolium <https://github.com/Telefonica/toolium>`_. 

The requirements to install Toolium are `Python 2.7 or 3.3+ <http://www.python.org>`_ and
`pip <https://pypi.python.org/pypi/pip>`_. If you use Python 2.7.9+, you don't need to install pip separately.

Clone `mc-qa-azure-17G <git@github.com:Telefonica/mc-qa-azure-17G.git>`_ repository and install requirements. It's
highly recommendable to use a virtualenv.

.. code:: console

    $ git clone git@github.com:Telefonica/mc-qa-azure-17G.git
    $ cd cd mc-qa-azure-17G
    $ python -m venv mc-qa-azure-17G-venv
    $ cd mc-qa-azure-17G-venv/
    $ source Scripts/activate
    $ pip install -r requirements.txt

It is also required an environment system variable WORKSPACE with the workspace path. For example

.. code:: console

    $ echo $WORKSPACE
    C:\workspace


Running Tests
-------------
To run a single test case (scenario):

.. code:: console

    $ behave -n "Test case name"
    
To run a feature file:

.. code:: console

    $ behave  "name.feature"
    
To run multiple feature files:

.. code:: console

    $ behave  "feature name 1.feature" "feature name 2.feature"
    





