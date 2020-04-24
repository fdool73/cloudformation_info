#!/usr/bin/env python3

# Print and/or save CloudFormation info
# Set region to AWS region CloudFormation stack is in

import boto3
import os
import json

region = ''

def main():
        param = input(str('Enter CloudFormation stack to search for: '))
        print('Searching...', flush=True)
        result = search_cf_stacks(param)
        try:
                info = describe_stack_resources(result)
                file_save(info)
        except IndexError:
                pass

# Search for and select CF stack 
def search_cf_stacks(param):
        client = boto3.client('cloudformation')
        paginator = client.get_paginator('describe_stacks')
        stacklist = []
        for response in paginator.paginate():
                for each in response['Stacks']:
                        if param in each['StackName']:
                                stacklist.append(each['StackName'])
                        else:
                                pass
        for index, value in enumerate(stacklist, 1):
                print("{}.{}".format(index, value))
        choose = int(input("\nEnter stack number to view resources: "))-1
        if choose < 0 or choose > (len(stacklist)-1):
                print('Invalid Choice')
        try:
                chosen = stacklist[choose]
                print(chosen)
        except IndexError:
                print('Number not in range')
        return(chosen)
                        
# Display all stack resources of CF stack (by name)
def describe_stack_resources(param):
        client = boto3.client('cloudformation')             
        response = client.describe_stack_resources(StackName = param)
        new_dict = {k: v for k,v in response.items()}
        result = new_dict['StackResources']
        print('Stack Name: ',result[0]['StackName'])
        print('Stack Id: ',result[0]['StackId'])
        print('Timestamp: ',result[0]['Timestamp'], '\n')
        for each in result:
                try:
                        stack_dict = {k: v for k, v in each.items()}
                        print('Resource Type: ',each['ResourceType'])
                        print('Logical Id: ',each['LogicalResourceId'])
                        print('Physical Resource Id: ',each['PhysicalResourceId'])
                        print('Resource Type: ',each['ResourceType'])
                        print('Status: ',each['ResourceStatus'], '\n')
                except KeyError:
                        print('/n')
        return(result[0]['StackName'],result)

# Save results to file 
def file_save(param):
        save = input('Save as file (y/n)?').lower()
        if save == 'y':
                reply = input(str('Current directory is "' + (os.getcwd()) + '" save here (y/n)?')).lower().strip()
                if reply == 'y':
                        filename = input(str('Enter filename to save: '))
                        with open(filename + '.txt', 'w') as filesave:
                                print('Saving to "' + (os.getcwd()) + '" - Done')
                                json.dump(param, filesave, indent=4, sort_keys=True, default=str)
                elif reply == 'n':
                        while True:
                                path = input(str('Enter location to save: ')).strip()
                                try:
                                        os.chdir(path)
                                except FileNotFoundError:
                                        print('Invalid path')

                                try:
                                        filename2 = input(str('Enter filename to save: ')).strip()
                                        with open(filename2 + '.txt', 'w') as filesave:
                                                print('Saving to "' + (os.getcwd()) + '" - Done')
                                                json.dump(param, filesave, indent=4, sort_keys=True, default=str)
                                                break
                                except PermissionError:
                                        print('Permission denied')
                else:
                        print('Please select (y)es or (n)o')
        elif save == 'n':
                return
        else:
                print('Please select (y)es or (n)o')
                return
        
if __name__ == "__main__":
        main()
