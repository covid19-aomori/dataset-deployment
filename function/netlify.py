from jeffy.framework import setup


app = setup()


@app.decorator.auto_logging
@app.decorator.sqs
def deploy(event, context):
    return event
