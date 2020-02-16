# -*- coding: utf-8 -*-

import os
import yaml
from unittest import TestCase
import shutil

# from toolium.behave.environment import (before_all as toolium_before_all, before_feature as toolium_before_feature,
#                                        before_scenario as toolium_before_scenario,
#                                        after_scenario as toolium_after_scenario,
#                                        after_feature as toolium_after_feature, after_all as toolium_after_all)


def before_all(context):
    """Initialization method that will be executed before the test execution

    :param context: behave context
    """
    # toolium_before_all(context)
    env_vars = yaml.load(open('environments.yml').read(), Loader=yaml.FullLoader)
    env = os.getenv('ENV', 'dev')
    context.env_vars = env_vars[env]
    context.testcase = TestCase()
    context.full_local_billing_files_path = os.environ["WORKSPACE"] + context.env_vars['LocalBillingFiles']

    # TBC --> Delete billing files from the current day --> summary, client and detail

def before_feature(context, feature):
    """Feature initialization

    :param context: behave context
    :param feature: running feature
    """
    # toolium_before_feature(context, feature)



def before_scenario(context, scenario):
    """Scenario initialization

    :param context: behave context
    :param scenario: running scenario
    """
    # toolium_before_scenario(context, scenario)


def after_scenario(context, scenario):
    """Clean method that will be executed after each scenario

    :param context: behave context
    :param scenario: running scenario
    """
    # toolium_after_scenario(context, scenario)


def after_feature(context, feature):
    """Clean method that will be executed after each feature

    :param context: behave context
    :param feature: running feature
    """
    # toolium_after_feature(context, feature)


def after_all(context):
    """Clean method that will be executed after all features are finished

    :param context: behave context
    """
    # toolium_after_all(context)

    #Delete content of the bilingFiles folder
    folder = context.full_local_billing_files_path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
