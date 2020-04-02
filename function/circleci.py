from jeffy.framework import setup
import boto3
import os
import requests
import urllib.parse


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

    project_slug = urllib.parse.quote('github/covid19-aomori/website')

    response = requests.post(
        f'https://circleci.com/api/v2/project/{project_slug}/pipeline',
        params={
            'branch': branch
        },
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
