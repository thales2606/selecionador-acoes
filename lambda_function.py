import json

def lambda_handler(event, context):
    # TODO implement
    print(event['teste'])
    return {
        'statusCode': 200,
        'body': event['teste']
    }