import boto3
import subprocess
import os

AWS_REGION = "ap-south-1"
STACK_NAME = "customer-rds-stack"
CODE_BUCKET = "customer-rds-code-bucket-ap-south-1"

def create_bucket():
    s3 = boto3.client("s3", region_name=AWS_REGION)

    try:
        s3.head_bucket(Bucket=CODE_BUCKET)
        print(f"Bucket {CODE_BUCKET} already exists")

    except Exception:
        print(f"Creating bucket {CODE_BUCKET}")

        if AWS_REGION == "ap-south-1":
            s3.create_bucket(Bucket=CODE_BUCKET)
        else:
            s3.create_bucket(
                Bucket=CODE_BUCKET,
                CreateBucketConfiguration={
                    "LocationConstraint": AWS_REGION
                }
            )

def upload_website():

    s3 = boto3.client("s3")

    files = [
    "website/index.html",
    "website/app.js",
    "website/style.css"
    ]

    for file in files:

        if os.path.exists(file):

            key = os.path.basename(file)
            s3.upload_file(
                file,
                CODE_BUCKET,
                f"website/{key}"
            )

            print(f"Uploaded {file}")


def sam_build():
    print("Running SAM Build")

    subprocess.run(
        "sam build",
        shell=True,
        check=True
    )


def sam_package():
    print("Running SAM Package")

    subprocess.run(
        f"sam package --s3-bucket {CODE_BUCKET} --output-template-file template-generated.yaml",
        shell=True,
        check=True
    )


def sam_deploy():
    print("Running SAM Deploy")

    subprocess.run(
        f"sam deploy --template-file template-generated.yaml --stack-name {STACK_NAME} --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND",
        shell=True,
        check=True
    )

def main():

    create_bucket()

    upload_website()

    sam_build()

    sam_package()

    sam_deploy()

print("Deployment completed successfully")


if __name__ == "__main__":
    main()
