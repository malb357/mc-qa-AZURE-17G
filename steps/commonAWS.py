# -*- coding: utf-8 -*-
import boto3
from behave import given, when, then
from requests_aws4auth import AWS4Auth
import requests
from botocore.exceptions import ClientError
import json
import logging
from datetime import date, timedelta


def get_today_summary_file_name(context):
    # today = date.today()
    # Check the S3 bucket has billing files from the current day
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(context.env_vars['billingBucketName'])
    summary_today_file_found = False

    today = date.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    second = last_month.replace(day=1)
    last_two_month = second - timedelta(days=1)

    if today.strftime("%m") == "1" and int(today.strftime("%d")) < 9:
        year = last_two_month.strftime("%Y")
    else:
        year = last_month.strftime("%Y")
    if int(today.strftime("%d")) < 9:
        month = last_two_month.strftime("%m")
        month_1 = last_month.strftime("%m")
    else:
        month = last_month.strftime("%m")
        month_1 = today.strftime("%m")

    print("billed/summary/{}-{}/{}{}{}".format(year, month, context.env_vars['prefixBillingSummaryFileName'], year, last_month.strftime("%m")))
    for obj in bucket.objects.all():
        if ("billed/summary/{}-{}/{}{}{}".format(year, month, context.env_vars['prefixBillingSummaryFileName'], year, month_1)) in obj.key:
            summary_today_file_found = True
            return obj.key

    if not summary_today_file_found:
        context.testcase.assertTrue(summary_today_file_found, msg='Billing files from today NOT FOUND')

def get_today_detail_file_name(context):
    # today = date.today()
    # Check the S3 bucket has billing files from the current day
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(context.env_vars['billingBucketName'])
    detail_today_file_found = False

    today = date.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    second = last_month.replace(day=1)
    last_two_month = second - timedelta(days=1)

    if today.strftime("%m") == "1" and int(today.strftime("%d")) < 9:
        year = last_two_month.strftime("%Y")
    else:
        year = last_month.strftime("%Y")
    if int(today.strftime("%d")) < 9:
        month = last_two_month.strftime("%m")
        month_1 = last_month.strftime("%m")
    else:
        month = last_month.strftime("%m")
        month_1 = today.strftime("%m")

    print("billed/detail/{}-{}/{}{}{}".format(year, month, context.env_vars['prefixBillingDetailFileName'], year, last_month.strftime("%m")))
    for obj in bucket.objects.all():
        if ("billed/detail/{}-{}/{}{}{}".format(year, month, context.env_vars['prefixBillingDetailFileName'], year, month_1)) in obj.key:
            detail_today_file_found = True
            return obj.key

    if not detail_today_file_found:
        context.testcase.assertTrue(detail_today_file_found, msg='Billing files from today NOT FOUND')

def get_consumption_file_name(context):
    today = date.today()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(context.env_vars['billingBucketName'])
    client_today_file_found = False

    for obj in bucket.objects.all():
        if (context.env_vars['consumptionFileName'] in obj.key) and (today.strftime("%Y-%m") in obj.key):
            client_today_file_found = True
            return obj.key

    if not client_today_file_found:
        context.testcase.assertTrue(client_today_file_found, msg='Consumption file from billing month NOT FOUND')


def get_today_client_file_name(context):
    today = date.today()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(context.env_vars['billingBucketName'])
    client_today_file_found = False

    for obj in bucket.objects.all():
        if (context.env_vars['prefixBillingClientFileName'] in obj.key) and (today.strftime("%Y%m%d") in obj.key):
            client_today_file_found = True
            return obj.key

    if not client_today_file_found:
        context.testcase.assertTrue(client_today_file_found, msg='Client billing files from today NOT FOUND')



@then('The status code is "{status_code}"')
def step_impl(context, status_code):
    print('expected status code ' + status_code)
    print('given status code {}'.format(context.response.status_code))
    context.testcase.assertEqual(context.response.status_code, int(status_code),
                                 msg="Status code invalid. Obtained {} instead of {}".format(
                                     context.response.status_code, status_code))


@then('the response has a json format')
def step_impl(context):
    try:
        json.loads(context.response.text)
    except Exception as e:
        context.logger.debug('Failed to convert to json format')
        context.testcase.assertTrue(False, msg='Error converting to json. Exception {}'.format(e))


@given('an AWS admin user')
def step_impl(context):
    # TBC with multienvironment
    logging.info('an AWS admin user')


@given('a OB with an AWS account')
def step_impl(context):
    # TBC with multienvironment
    logging.info('a OB with an AWS account')
