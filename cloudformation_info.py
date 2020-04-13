#!/usr/bin/env python3

import boto3

def describe_cf_stacks():
    client = boto3.client('cloudformation')
    paginator = client.get_paginator('describe_stacks')
    response = paginator.paginate()
    for each in response:
        stack = each['Stacks']
        for i in stack:
                try:
                        print('Stack Name: ',i['StackName'])
                        print('Description: ',i['Description'])
                        print('Creation Time: ',i['CreationTime'])
                        print('Deletion Time: ',i['DeletionTime'])
                        print('Stack Status: ',i['StackStatus'], '\n')
                except KeyError:
                        print('\n')
                        
def search_cf_stacks(param):
    client = boto3.client('cloudformation')
    paginator = client.get_paginator('describe_stacks')
    response = paginator.paginate()
    for each in response:
            stack = each['Stacks']
            for i in stack:
                if param in i['StackName']:
                        try:
                                print('Stack Name: ',i['StackName'])
                                print('Description: ',i['Description'])
                                print('Creation Time: ',i['CreationTime'])
                                print('Deletion Time: ',i['DeletionTime'])
                                print('Stack Status: ',i['StackStatus'], '\n')
                        except KeyError:
                                print('\n')

def describe_stack_resources(param):
    client = boto3.client('cloudformation')             
    response = client.describe_stack_resources(StackName = param)
    new_dict = {k: v for k,v in response.items()}
    result = new_dict['StackResources']
    print('Stack Name: ',result[0]['StackName'])
    print('Stack Id: ',result[0]['StackId'])
    print('Timestamp: ',result[0]['Timestamp'], '\n')
    for each in result:
        stack_dict = {k: v for k, v in each.items()}
        print('Resource Type: ',each['ResourceType'])
        print('Logical Id: ',each['LogicalResourceId'])
        print('Physical Resource Id: ',each['PhysicalResourceId'])
        print('Resource Type: ',each['ResourceType'])
        print('Status: ',each['ResourceStatus'], '\n')

print('Enter selection: ','\n', '1. Drescribe all CF stacks', '\n', '2. Search for CF stack', '\n', '3. List CF resources')

while True:
        try:
                selection = int(input("Make selection: "))
        except ValueError:
                print("Invalid choice, select 1, 2 or 3")
                continue
        else:
                break
if selection == 1:
        describe_cf_stacks()
elif selection == 2:
        stack = input("Search: ")
        search_cf_stacks(stack)
elif selection == 3:
        resource = input("Enter stack name: ")
        describe_stack_resources(resource)
else:
        print("Invalid selection")
