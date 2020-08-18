# -*- coding: utf-8 -*-
import boto3
from behave import given, when, then
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
import logging
import time
import csv
from steps.commonAWS import get_today_summary_file_name, get_today_detail_file_name, get_today_client_file_name, get_consumption_file_name
import shutil
from datetime import date, timedelta
import os
import gzip
import csv


@when('generateBilling is executed with boto')
def step_impl(context):
    # Execute the lambada with Boto and  
    auth = BotoAWSRequestsAuth(aws_host=context.env_vars['awsApiHost'],
                               aws_region=context.env_vars['region'],
                               aws_service='execute-api')
    params = {'force': 'true', 'offset': '1', 'regenerateWithCorrections': 'true'}
    context.generate_billing_response = requests.get(context.env_vars['generateBillingURL'], auth=auth, params=params, timeout=30)
    # If timeout we have to wait until the lambda
    status_code_gateway_timeout = 504
    if context.generate_billing_response.status_code == status_code_gateway_timeout:
        time.sleep(context.env_vars['generateBillingTimeoutSleep'])
    
@when('generateBilling with includeRef with value false is executed with boto')
def step_impl(context):
    # Execute the lambada with Boto and  
    auth = BotoAWSRequestsAuth(aws_host=context.env_vars['awsApiHost'],
                               aws_region=context.env_vars['region'],
                               aws_service='execute-api')
    params = {'force': 'true', 'includeRef': 'false', 'regenerateWithCorrections': 'true', 'offset': '1'}
    context.generate_billing_response = requests.get(context.env_vars['generateBillingURL'], auth=auth, params=params, timeout=30)
    # If timeout we have to wait until the lambda
    status_code_gateway_timeout = 504
    if context.generate_billing_response.status_code == status_code_gateway_timeout:
        time.sleep(context.env_vars['generateBillingTimeoutSleep'])

@when('generateBilling with includeRef with value true is executed with boto')
def step_impl(context):
    # Execute the lambada with Boto and  
    auth = BotoAWSRequestsAuth(aws_host=context.env_vars['awsApiHost'],
                               aws_region=context.env_vars['region'],
                               aws_service='execute-api')
    params = {'force': 'true', 'includeRef': 'true', 'regenerateWithCorrections': 'true', 'offset': '1'}
    context.generate_billing_response = requests.get(context.env_vars['generateBillingURL'], auth=auth, params=params, timeout=30)
    # If timeout we have to wait until the lambda
    status_code_gateway_timeout = 504
    if context.generate_billing_response.status_code == status_code_gateway_timeout:
        time.sleep(context.env_vars['generateBillingTimeoutSleep'])


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

@then('summary file header were correctly generated')
def step_impl(context):
    # Download the csv summary files
    expected_set = set(context.env_vars["csvSummaryHeaders"])
    csv = "{}/{}".format(context.full_local_billing_files_path, context.summary_file_name.split("/")[3])
    print(csv)
    first_line = None
    with open(csv, "r") as csv_file:
        first_line = csv_file.readline()
    first_line_set = set(first_line.replace("\n","").split(","))
    # print(first_line)
    # print(first_line.split(","))
    # print(context.env_vars["csvSummaryHeaders"])
    # print(expected_set.difference(first_line_set))
    assert expected_set.difference(first_line_set) == set()

@then('detail file header were correctly generated')
def step_impl(context):
    # Download the csv summary files
    expected_set = set(context.env_vars["csvDetailHeaders"])
    csv = "{}/{}".format(context.full_local_billing_files_path, context.detail_file_name.split("/")[3])
    print(csv)
    first_line = None
    with gzip.open(csv, 'rt', encoding='utf8') as csv_zip:
        first_line = csv_zip.readline()
    first_line_set = set(first_line.replace("\n","").split(","))
    print("First line set: {}".format(first_line_set))
    print("expected set: {}".format(expected_set))
    # print(first_line.split(","))
    # print(context.env_vars["csvSummaryHeaders"])
    print("DIFERENCIA: {}".format(expected_set.difference(first_line_set)))
    assert expected_set.difference(first_line_set) == set()

@then('today summary file is downloaded')
def step_impl(context):
    s3 = boto3.client('s3')
    # Download the csv summary files
    context.summary_file_name = get_today_summary_file_name(context)
    # print(context.summary_file_name)
    # print(context.summary_file_name.split("/")[3])
    csv_file_name = context.summary_file_name.split("/")[3]
    s3.download_file(context.env_vars['billingBucketName'], context.summary_file_name, csv_file_name)
    # Move the csv to the billingFiles folder
    # print("{}".format(csv_file_name))
    # print("{}/{}".format(context.full_local_billing_files_path, csv_file_name))
    shutil.move(csv_file_name, "{}/{}".format(context.full_local_billing_files_path, csv_file_name))

@then('today detail file is downloaded')
def step_impl(context):
    s3 = boto3.client('s3')
    # Download the csv detail files
    context.detail_file_name = get_today_detail_file_name(context)
    # print(context.detail_file_name)
    # print(context.detail_file_name.split("/")[3])
    csv_file_name = context.detail_file_name.split("/")[3]
    s3.download_file(context.env_vars['billingBucketName'], context.detail_file_name, csv_file_name)
    # Move the csv to the billingFiles folder
    # print("{}".format(csv_file_name))
    # print("{}/{}".format(context.full_local_billing_files_path, csv_file_name))
    shutil.move(csv_file_name, "{}/{}".format(context.full_local_billing_files_path, csv_file_name))

@then('consumption file is downloaded')
def step_impl(context):
    s3 = boto3.client('s3')
    # Download the csv detail files
    context.consumption_file_name = get_consumption_file_name(context)
    # print(context.detail_file_name)
    # print(context.detail_file_name.split("/")[3])
    csv_file_name = context.consumption_file_name.split("/")[2]
    s3.download_file(context.env_vars['billingBucketName'], context.consumption_file_name, csv_file_name)
    # Move the csv to the billingFiles folder
    # print("{}".format(csv_file_name))
    # print("{}/{}".format(context.full_local_billing_files_path, csv_file_name))
    shutil.move(csv_file_name, "{}/{}".format(context.full_local_billing_files_path, csv_file_name))

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


@then('charge value is correct')
def step_impl(context):
    detail_file_name = "{}/{}".format(context.full_local_billing_files_path, context.detail_file_name.split("/")[3])
    consumption_file_name = "{}/{}".format(context.full_local_billing_files_path, context.consumption_file_name.split("/")[2])
    print(detail_file_name)
    print(consumption_file_name)
    with gzip.open(detail_file_name, 'rt', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['chargeType'] == "azure_consumption" and float(row['charge']) > 0:
                quantity_detail = round(float(row['quantity']), 2)
                charge_detail_file = round(float(row['charge']), 2)
                resourceId_detail = row['resourceId']
                productId, skuId, _ = resourceId_detail.split("-")
                break

    with open(consumption_file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ProductId'] == productId and row['SkuId'] == skuId:
                unit_price = round(float(row['UnitPrice']), 2)
                break
    context.testcase.assertEquals(round(unit_price*quantity_detail, 2), charge_detail_file,  msg="Charge is not ok. Obtained {} instead of {}".format(round(unit_price*quantity_detail, 2), charge_detail_file))
     


@then('the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info')
def step_impl(context):
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

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])

    response = table.get_item(
        Key=context.env_vars['dynamoDBPrimaryKey']
    )
    print("lastAzureInvoiceDate {}".format(response["Item"]["lastAzureInvoiceDate"]))
    print("lastAzureInvoiceDate {}".format(response["Item"]["billingFileDate"]))
    item = response['Item']
    last_azure_invoice_date = item['lastAzureInvoiceDate']
    billing_file_date = item['billingFileDate']

    print("Date: {}{}01".format(year, month))

    context.testcase.assertTrue("{}{}01".format(year, month_1) in last_azure_invoice_date, msg=today.strftime(
        "%Y%m") + "01 - Not found in dyanmoDB last_azure_invoice_date: " + last_azure_invoice_date)
    context.testcase.assertIsNotNone(billing_file_date, msg="billingFileDate is empty")
