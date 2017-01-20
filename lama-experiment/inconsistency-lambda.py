import os
def lambda_handler(event, context):
    return {"id": [os.getenv("CID")]}
