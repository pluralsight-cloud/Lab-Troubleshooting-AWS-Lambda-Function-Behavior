import boto3
import urllib.request
import urllib3
import json


s3 = boto3.client("s3")
http = urllib3.PoolManager()

def send_response(event, context, status):

    response = {
        "Status": status,
        "Reason": "Image loading process completed",
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"]
    }

    http.request(
        "PUT",
        event["ResponseURL"],
        body=json.dumps(response).encode("utf-8"),
        headers={
            "content-type": ""
        }
    )

def handler(event, context):

    if event["RequestType"] == "Delete":
        send_response(event, context, "SUCCESS")
        return

    bucket = event["ResourceProperties"]["Bucket"]

    base_url = (
        "https://raw.githubusercontent.com/"
        "pluralsight-cloud/"
        "Lab-Troubleshooting-AWS-Lambda-Function-Behavior/"
        "main/Images"
    )

    files = [
        "Donkey.png",
        "Kitty.png",
        "Parakeet.png",
        "Puppy.png"
    ]


    try:

        for filename in files:

            url = f"{base_url}/{filename}"

            image_data = urllib.request.urlopen(url).read()


            s3.put_object(
                Bucket=bucket,
                Key=filename,
                Body=image_data,
                ContentType="image/png"
            )


        send_response(event, context, "SUCCESS")


    except Exception as error:

        print(error)

        send_response(event, context, "FAILED")