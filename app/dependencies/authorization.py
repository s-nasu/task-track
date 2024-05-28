import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader

from config import settings

api_key_header = APIKeyHeader(name="Authorization", auto_error=True)


def verify_token(auth_header: str = Depends(api_key_header)):
    if auth_header != "expected_token":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication token",
        )


def get_user_from_token(
    auth_header: str, user_pool_id: str = settings.customer_side_user_pool_id
):
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization header not found",
        )
    bearer, _, access_token = auth_header.partition(" ")
    if bearer != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme",
        )
    try:
        client = boto3.client("cognito-idp")

        user_response = client.get_user(AccessToken=access_token)
        user_id = user_response["Username"]

        admin_response = client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=user_id,
        )

        user_attributes = {
            item["Name"].replace("custom:", ""): item["Value"]
            for item in admin_response["UserAttributes"]
        }

        result = {"user_id": user_id, **user_attributes}
        return result

    except (BotoCoreError, ClientError) as e:

        if e.response["Error"]["Code"] == "NotAuthorizedException":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
            )
        elif e.response["Error"]["Code"] == "UserNotFoundException":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )


def get_user_info(request: Request, auth_header: str = Depends(api_key_header)):
    return get_user_from_token(auth_header)
