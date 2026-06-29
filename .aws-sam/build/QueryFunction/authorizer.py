import os

def generate_policy(principal_id, effect, resource):
    """
    Generate IAM policy for API Gateway
    """


    return {
        "principalId": principal_id,
        "policyDocument": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "execute-api:Invoke",
                "Effect": effect,
                "Resource": resource
            }
            ]
        }
    }


def lambda_handler(event, context):
    print("Authorizer Event:", event)

    try:

            token = event.get("authorizationToken")

            expected_token = os.environ.get(
            "AUTH_TOKEN",
            "my-secret-token"
            )

            if token == expected_token:

                print("Authorization Success")

            return generate_policy(
                principal_id="customer-user",
                effect="Allow",
                resource=event["methodArn"]
        )

            print("Authorization Failed")
            return generate_policy(
            principal_id="customer-user",
            effect="Deny",
            resource=event["methodArn"]
        )
    except Exception as e:

        print(f"Authorizer Error: {str(e)}")

        return generate_policy(
            principal_id="customer-user",
            effect="Deny",
            resource=event["methodArn"]
        )

