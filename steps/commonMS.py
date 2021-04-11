# -*- coding: utf-8 -*-
from behave import given, when, then
import requests
import json
import logging
from datetime import date, timedelta

def partner_center_authentication(context):
    client_id = context.env_vars['ms_client_id']
    client_secret = context.env_vars['ms_client_secret']

    url = "https://login.windows.net/movilesargentinacsp.onmicrosoft.com/oauth2/token?api-version=1.0"

    payload={'grant_type': 'client_credentials',
    'resource': 'https://graph.windows.net',
    'client_id': client_id,
    'client_secret': client_secret}
    files=[]
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'fpc=ApqDEfWFOEBPmjkcYpeGydPETM9UAQAAAOLX1tcOAAAAom3TfgIAAADE2NbXDgAAAKSjRmkBAAAA8djW1w4AAAA; stsservicecookie=estsfd; x-ms-gateway-slice=prod'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    json = response.json()


    return json.get('access_token')



def get_invoice_line_items(context):
    # url related to a specific invoice
    url = "https://api.partnercenter.microsoft.com/v1/invoices/D0500034MV/lineitems?provider=office&invoicelineitemtype=billinglineitems"

    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(context.ms_token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    #print("Response:")
    #print(response.text)

    return response.json()