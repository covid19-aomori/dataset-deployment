from jeffy.framework import setup
import boto3
import os
import requests
import json


app = setup()

product_id = os.environ.get('ProductId')
env = os.environ.get('Env')


@app.decorator.auto_logging
@app.decorator.sqs
def call_pipeline(event, context):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name=f'/{product_id}/{env}/circleci/token',
        WithDecryption=True
    )
    circleci_token = response['Parameter']['Value']

    branch = 'development'
    if env == 'production':
        branch = 'master'
    app.logger.info({'branch': branch})

    response = requests.post(
        'https://circleci.com/api/v2/project/github/covid19-aomori/website/pipeline',
        data=json.dumps({
            'branch': branch
        }),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Circle-Token': circleci_token
        }
    )

    return {
        'reason': response.reason,
        'status_code': response.status_code
    }
