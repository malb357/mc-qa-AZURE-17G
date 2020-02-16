# -*- coding: utf-8 -*-
import boto3
from behave import given, when, then
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
import logging
import time
import csv
from steps.commonAWS import get_today_summary_file_name, get_today_detail_file_name, get_today_client_file_name
import shutil
from datetime import date
import os


@when('generateBilling is executed with boto')
def step_impl(context):
    # Execute the lambada with Boto and
    auth = BotoAWSRequestsAuth(aws_host=context.env_vars['awsApiHost'],
                               aws_region=context.env_vars['region'],
                               aws_service='execute-api')
    params = {'force': 'true'}
    context.generate_billing_response = requests.get(context.env_vars['generateBillingURL'], auth=auth, params=params)
    # If timeout we have to wait until the lambda
    status_code_gateway_timeout = 504
    if context.generate_billing_response.status_code == status_code_gateway_timeout:
        time.sleep(context.env_vars['generateBillingTimeoutSleep']),


@then('today summary, a client and a detail file are downloaded')
def step_impl(context):
    s3 = boto3.client('s3')

    # Download the csv summary files
    csv_file_name = context.summary_file_name.split("/")[1]
    s3.download_file(context.env_vars['billingBucketName'], context.summary_file_name, csv_file_name)
    # Move the csv to the billingFiles folder
    shutil.move(csv_file_name, context.full_local_billing_files_path)

    # Download the csv client files
    csv_file_name = context.client_today_file_name.split("/")[1]
    s3.download_file(context.env_vars['billingBucketName'], context.client_today_file_name, csv_file_name)
    shutil.move(csv_file_name, context.full_local_billing_files_path)

    # Download the csv detail files
    csv_file_name = context.detail_today_file_name.split("/")[1]
    s3.download_file(context.env_vars['billingBucketName'], context.detail_today_file_name, csv_file_name)
    shutil.move(csv_file_name, context.full_local_billing_files_path)


@then('the answer to the lambda generateBilling is OK')
def step_impl(context):
    # Check response to generateBilling (if timeout give a warning)
    status_code = 200
    status_code_gateway_timeout = 504
    if context.generate_billing_response.status_code == status_code_gateway_timeout:
        logging.warning("ApiGateway Timeout- StatusCode: " + str(context.generate_billing_response.status_code))
    else:
        context.testcase.assertEquals(context.generate_billing_response.status_code, status_code,
                                      msg="Status code invalid. Obtained {} instead of {}".format(
                                          context.generate_billing_response.status_code, status_code))

@then('the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info')
def step_impl(context):
    today = date.today()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])

    response = table.get_item(
        Key=context.env_vars['dynamoDBPrimaryKey']
    )

    item = response['Item']
    last_aws_invoice_date = item['lastAWSInvoiceDate']
    billing_file_date = item['billingFileDate']

    context.testcase.assertTrue(today.strftime("%Y%m") + "01" in last_aws_invoice_date, msg=today.strftime(
        "%Y%m") + "01 - Not found in dyanmoDB last_aws_invoice_date: " + last_aws_invoice_date)
    context.testcase.assertIsNotNone(billing_file_date, msg="billingFileDate is empty")
