# -*- coding: utf-8 -*-
from behave import given, when, then
import requests
import json
import logging
from datetime import date, timedelta


def partner_center_authentication_cost_management(context):

    client_id = context.env_vars['ms_client_id']
    client_secret = context.env_vars['ms_client_secret']
    refresh_token = context.env_vars['ms_refresh_token']

    url = "https://login.microsoftonline.com/movilesargentinacsp.onmicrosoft.com/oauth2/token"

    payload = {'grant_type': 'refresh_token',
               'client_id': client_id,
               'client_secret': client_secret,
               'resource': "https://management.core.windows.net",
               'refresh_token': refresh_token
               }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Cookie': 'buid=0.AREADQSIkWdsW0yxEjajBLZtrXbeMWemFK5Jl7xuumkUOR4zAAA.AQABAAEAAAD--DLA3VO7QrddgJg7Wevr8e8E7XkduKKMZuer76H_2wldNWGEd-jP3mVMbBAOCPYZoTLMAoITq2IuXu0Nsviyt_VEOZIy5xvDMBjvTkU1wE4nZGE-ZDX5VVnQQg-BA4IgAA; fpc=Am7pj9MJ_H9OoPlKblTFeKv0GUUHAQAAAOb0INgOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    # print(json_data)
    context.access_token_pc = json_data.get('access_token')
    return json_data.get('access_token')


def cost_management_query(context):
    ACCESS_TOKEN_PC = context.access_token_pc

    url = "https://management.azure.com/providers/Microsoft.Billing/billingAccounts/3adfe2ce-e3d9-4640-8772-6cba000a4e44:c836119f-b080-4834-8dac-a64a8daa0024_2018-09-30/providers/Microsoft.CostManagement/query?api-version=2019-11-01"
    
    # Update the timePeriod for the current month

    payload = json.dumps(
        {
            "type": "ActualCost",
            "timeframe": "Custom",
            "timePeriod": {
                "from": "2021-03-01",
                "to": "2021-03-31"
            },
            "dataset": {
                "granularity": "None",
                "aggregation": {
                    "totalQty": {
                        "name": "UsageQuantity",
                        "function": "Sum"
                    },
                    "totalCostUSD": {
                        "name": "CostUSD",
                        "function": "Sum"
                    }
                },
                "grouping": [
                    {
                        "type": "Dimension",
                        "name": "customerTenantId"
                    },
                    {
                        "type": "Dimension",
                        "name": "PublisherType"
                    },
                    {
                        "type": "Dimension",
                        "name": "ChargeType"
                    },
                    {
                        "type": "Dimension",
                        "name": "ServiceName"
                    },
                    {
                        "type": "Dimension",
                        "name": "ResourceGuid"
                    },
                    {
                        "type": "Dimension",
                        "name": "UnitOfMeasure"
                    },
                    {
                        "type": "Dimension",
                        "name": "partnerEarnedCreditApplied"
                    },
                    {
                        "type": "Dimension",
                        "name": "product"
                    },
                    {
                        "type": "Dimension",
                        "name": "ResourceLocation"
                    },
                    {
                        "type": "Dimension",
                        "name": "ReservationName"
                    },
                    {
                        "type": "Dimension",
                        "name": "Frequency"
                    },
                    {
                        "type": "Dimension",
                        "name": "PricingModel"
                    }
                ]
            }
        }
    )

    files = []
    headers = {
        'Authorization': 'Bearer {}'.format(ACCESS_TOKEN_PC),
        'Content-Type': 'application/json'
    }

    next_link = True
    response_data = []

    while next_link == True:
        response = requests.request("POST", url, headers=headers, data=payload)
        json_response = response.json()
        response_data.extend(json_response.get('properties').get('rows'))
        print("length: {}".format(len(response_data)))
        if json_response.get('properties').get('nextLink') != "":
            next_link = True
            url = json_response['properties']['nextLink']
            print("Next Link: {}".format(next_link))
            print("Url: {}".format(url))
        else:
            next_link = False

    # print("Response data: {}".format(response_data))
    return response_data
