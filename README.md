# mc-qa-azure-17G

The aim of this project is create a set of automatic functional tests for the the New Azure Experience sku 17G.
The test cases are developed in Python wrapper tool Toolium using Behave. 

What is Behave?
It's a behavior-driven development (BDD), Python style. For more detail about BDD check https://behave.readthedocs.io/en/latest/philosophy.html

----

## Getting Started

This project was started from `Toolium <https://github.com/Telefonica/toolium>`

The requirements to install Toolium are [Python 2.7 or 3.3+](http://www.python.org) and
[pip](https://pypi.python.org/pypi/pip). If you use Python 2.7.9+, you don't need to install pip separately.

Clone mc-qa-azure-17G repository and install requirements. It's
highly recommendable to use a virtualenv.


```bash
git clone git@github.com:Telefonica/mc-qa-azure-17G.git
cd mc-qa-azure-17G
python3 -m venv mc-qa-azure-17G-venv
cd mc-qa-azure-17G-venv/
source Scripts/activate
pip3 install -r requirements.txt
```

It is also required an environment system variable WORKSPACE with the workspace path. For example

```bash
echo $WORKSPACE
C:\workspace
```

## Running Tests

To run a single test case (scenario):

```bash
behave -n "Test case name"
```
    
To run a feature file:

```bash
behave  "name.feature"
```
    
To run multiple feature files:

```bash
behave  "feature name 1.feature" "feature name 2.feature"
```    





