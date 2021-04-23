# -*- coding: utf-8 -*-
import boto3
from behave import given, when, then
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta


@given('an aws credentials for dynamodb')
def step_impl(context):
    # Get the service resource.
    context.dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

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

@then('billed detail files with "{offset_a}" exists')
def step_impl(context,offset_a):
        
    mes=context.env_vars['offset_a'] + 1 
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(context.env_vars['billingBucketName'])
    detail_file_found = False
    today = date.today() - relativedelta(months=mes) 
    year = today.strftime("%Y")
    month =  today.strftime("%m") 

    # Busca el fichero aws_detail_[OB]
    for obj in bucket.objects.all():
        ruta=context.env_vars['reportPrefixBilled'] + "/" + context.env_vars['reportNameDetail'] + "/" + year + "-" + month + "/" + context.env_vars['prefixBillingDetailFileName']
        if (ruta in obj.key):               
            detail_file_found = True
            print("Detail Billed file FOUND:", obj.key)

    # Si no se encuentra el fichero detail, salimos        
    if not detail_file_found:
        context.testcase.assertTrue(detail_file_found, print("Detail Billed file NOT FOUND"))

    return obj.key

@then('detail files with "{offset_b}" exists')
def step_impl(context,offset_b):
        
    mes=context.env_vars['offset_b'] + 1 
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(context.env_vars['billingBucketName'])
    detail_file_found = False
    today = date.today() - relativedelta(months=mes) 
    year = today.strftime("%Y")
    month =  today.strftime("%m") 

    # Busca el fichero aws_detail_[OB]
    for obj in bucket.objects.all():
        ruta=context.env_vars['reportPrefixBilled'] + "/" + context.env_vars['reportNameDetail'] + "/" + year + "-" + month + "/" + context.env_vars['prefixBillingDetailFileName']
        if (ruta in obj.key):               
            detail_file_found = True
            print("Detail Billed file FOUND:", obj.key)

    # Si no se encuentra el fichero detail, salimos        
    if not detail_file_found:
        context.testcase.assertTrue(detail_file_found, print("Detail Billed file NOT FOUND"))

    return obj.key

@given('priceFactor is updated with "{newPriceFactor}" in DynamoDB')
def step_impl(context,newPriceFactor):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response # the response is in the form of a dictionary

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            priceFactor = context.dict['Items'][contador]['priceFactor']
            update_newPriceFactor = context.env_vars['newPriceFactor']
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set priceFactor = :newPriceFactor",
                ExpressionAttributeValues={
                    ':newPriceFactor': str(update_newPriceFactor),
                },
                #ReturnValues="UPDATED_NEW"
            )                      
        contador=contador+1
        
@given('priceFactor is updated with invalidPriceFactor "{invalidPriceFactor}" in DynamoDB')
def step_impl(context,invalidPriceFactor):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response # the response is in the form of a dictionary

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            context.env_vars['old_priceFactor'] = context.dict['Items'][contador]['priceFactor']
            update_newPriceFactor = context.env_vars['invalidPriceFactor']
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set priceFactor = :invalidPriceFactor",
                ExpressionAttributeValues={
                    ':invalidPriceFactor': str(update_newPriceFactor),
                },
                #ReturnValues="UPDATED_NEW"
            )                      
        contador=contador+1

@given('BucketName is updated with invalidBucketName in DynamoDB')
def step_impl(context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response # the response is in the form of a dictionary

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            context.env_vars['old_bucketName'] = context.dict['Items'][contador]['bucketName']
            update_newBucketName = "prebilling-invalid"
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set bucketName = :invalidBucketName",
                ExpressionAttributeValues={
                    ':invalidBucketName': str(update_newBucketName),
                },
            )                      
        contador=contador+1


@given('language is updated with ES in DynamoDB')
def step_impl(context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response # the response is in the form of a dictionary

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            context.env_vars['old_lang'] = context.dict['Items'][contador]['lang']
            update_newLanguage = "ES"
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set lang = :newLang",
                ExpressionAttributeValues={
                    ':newLang': str(update_newLanguage),
                },
                #ReturnValues="UPDATED_NEW"
            )                      
        contador=contador+1  

@given('language is updated with EN in DynamoDB')
def step_impl(context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response # the response is in the form of a dictionary

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            context.env_vars['old_lang'] = context.dict['Items'][contador]['lang']
            update_newLanguage = "EN"
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set lang = :newLang",
                ExpressionAttributeValues={
                    ':newLang': str(update_newLanguage),
                },
                #ReturnValues="UPDATED_NEW"
            )                      
        contador=contador+1  

@given('language is updated with INVALID in DynamoDB')
def step_impl(context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response # the response is in the form of a dictionary

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            context.env_vars['old_lang'] = context.dict['Items'][contador]['lang']
            update_newLanguage = "INVALID"
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set lang = :newLang",
                ExpressionAttributeValues={
                    ':newLang': str(update_newLanguage),
                },
            )                      
        contador=contador+1

@then('restore language in DynamoDB')
def step_impl(context):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            update_newLanguage = context.env_vars['old_lang']
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set lang = :newLang",
                ExpressionAttributeValues={
                    ':newLang': str(update_newLanguage),
                },
            )                      
        contador=contador+1 

@then('restore bucketName in DynamoDB')
def step_impl(context):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            update_newBucketName = context.env_vars['old_bucketName']
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set bucketName = :newBucketName",
                ExpressionAttributeValues={
                    ':newBucketName': str(update_newBucketName),
                },
            )                      
        contador=contador+1 

@then('restore priceFactor in DynamoDB')
def step_impl(context):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(context.env_vars['dynamoDbName'])
    response = table.scan()
    context.dict = response

    #buscamos la entrada configId=current en la tabla de configuración de dynamoDB
    contador=0
    for current in context.dict['Items']:
        actual = context.dict['Items'][contador]['configId']
        if (actual=="current"):
            update_newPriceFactor = context.env_vars['old_priceFactor']
            response = table.update_item(
                Key={
                    'configId': actual
                },
                UpdateExpression="set priceFactor = :newPriceFactor",
                ExpressionAttributeValues={
                    ':newPriceFactor': str(update_newPriceFactor),
                },
            )                      
        contador=contador+1 