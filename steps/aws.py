# -*- coding: utf-8 -*-
import boto3
from behave import given, when, then


@given('an aws credentials for dynamodb')
def step_impl(context):
    # Get the service resource.
    context.dynamodb = boto3.resource('dynamodb')

@given('an aws credentials for s3')
def step_impl(context):
    # Get the service resource.
    context.s3 = boto3.resource('s3')

@when('the database "{db_name}" is not empty')
def step_impl(context, db_name):
    print(db_name)
    table = context.dynamodb.Table(db_name)
    response = table.scan()
    context.dict= response # the response is in the form of a dictionary

@then('the content of the db is shown')
def step_impl(context):
   print(context.dict)

@when('the bucket "{bucket_name}" is not empty')
def step_impl(context, bucket_name):
    context.bucket = context.s3.Bucket(bucket_name)

@then ('a list of objects names are shown')
def step_impl(context):
    for obj in context.bucket.objects.all():
        print(obj.key, obj.last_modified)