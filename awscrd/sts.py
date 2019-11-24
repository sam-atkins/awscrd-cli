"""
Interface via Boto3 to a low-level client representing AWS
Security Token Service (STS)
"""
import boto3
import sys
from typing import Mapping


def get_token(
    token: str, aws_iam_account_number: str, username: str
) -> Mapping[str, str]:
    """
    Uses boto to make a request to STS to get a session token and other security
    credentials

    Args:
        token (str): MFA token
        aws_iam_account_number (str): the profile's AWS IAM account number
        username (str): the user's AWS username

    Returns:
        Mapping: Credentials from the STS response
    """
    client = boto3.client("sts")

    arn_string = f"arn:aws:iam::{aws_iam_account_number}:mfa/{username}"

    try:
        response = client.get_session_token(
            DurationSeconds=129600, SerialNumber=arn_string, TokenCode=token
        )
    # TODO(sam) narrow down to boto exception
    except Exception as ex:
        print(f"❌ Request to STS failed: {ex}")
        sys.exit(1)

    creds = response.get("Credentials")
    if creds is None:
        print("❌ Something went wrong with the STS request")
        sys.exit(1)

    return creds