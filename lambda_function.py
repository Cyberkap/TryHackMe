import os
from openai import OpenAI

client = OpenAI()
import boto3
import json

os.environ["OPENAI_API_KEY"] = "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"

def lambda_handler(event, context):
    try:
        s3_bucket = 's3bucket97'
        s3_key = 'securityhub-findings/'  # Update to the actual path where Security Hub findings are stored

        s3 = boto3.client('s3')
        s3_response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
        securityhub_findings = json.loads(s3_response['Body'].read().decode('utf-8'))

        user_input = event.get('body')  # Adjust to match how Amplify sends data
        user_input = json.loads(user_input).get('input')  # Adjust based on your Amplify request structure
        if not user_input:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': 'Input is missing'})
            }

        # Call OpenAI GPT-3.5-turbo
        response = client.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": json.dumps(securityhub_findings)}
        ])

        # Extract response from OpenAI
        chat_gpt_response = response['choices'][0]['message']['content']

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust based on your CORS policy
                'Content-Type': 'application/json',
            },
            'body': json.dumps({'response': chat_gpt_response})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }
