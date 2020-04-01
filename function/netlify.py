from jeffy.framework import setup
# import boto3
import os
# import requests


app = setup()

product_id = os.environ.get('ProductId')
env = os.environ.get('Env')


@app.decorator.auto_logging
@app.decorator.sqs
def deploy(event, context):
    """
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name=f'/{product_id}/{env}/netlify/build_hook_url',
        WithDecryption=True
    )
    netlify_build_hook_url = response['Parameter']['Value']

    response = requests.post(netlify_build_hook_url)

    return {
        'reason': response.reason,
        'status_code': response.status_code
    }
    """

    return {
        'reason': 'とりあえず何もしないよ',
        'status_code': 200
    }
