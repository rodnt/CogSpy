import boto3
from botocore.exceptions import ClientError

class CognitoClient:
    def __init__(self, region,client_id="",pool_id="",identity_id="",code=""):
        """
        Initialize the CognitoClient with the necessary Cognito configuration.
        :param region: AWS region where the Cognito User Pool is located.
        :param client_id: Client ID for the Cognito User Pool application.
        """
        self.region = region
        self.client_id = client_id
        self.id_pool_id = pool_id
        self.identity_id = identity_id
        self.confirmation_code = code
        self.client = boto3.client('cognito-idp', region_name=self.region)
        self.identity_client = boto3.client('cognito-identity', region_name=self.region)
        self.user_pools_client = boto3.client('cognito-idp', region_name=self.region)

    def register(self, username, password, email):
        """
        Sign up a new user with Cognito User Pool.
        :param username: Username for the new user.
        :param password: Password for the new user.
        :param email: Email address for the new user.
        """
        try:
            response = self.client.sign_up(
            ClientId=self.client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    }
                ]
            )
            print("User sign-up successful.")
            print(response)
            if response.get('UserConfirmed', False):
                print(f"\n>>> [HIGH] Registration without confirmation detected. [DOS - New Users]")
            
        except ClientError as e:
            print(f"An error occurred: {e}")
    
    def confirm_user(self, username, confirmation_code):
        """
        Confirm a new user's sign-up process using the confirmation code they received.
        :param username: Username of the user to confirm.
        :param confirmation_code: The confirmation code received by the user.
        """
        try:
            response = self.client.confirm_sign_up(
                ClientId=self.client_id,
                Username=username,
                ConfirmationCode=confirmation_code
            )
            print("User confirmation successful.")
            print(response)
        except ClientError as e:
            print(f"An error occurred: {e}")

    def generate_identity_id(self, identity_pool_id):
        """
        Generate an identity ID using the given identity pool ID.
        :param identity_pool_id: The ID of the Cognito Identity Pool.
        :return: The generated identity ID or None if an error occurred.
        """
        try:
            response = self.identity_client.get_id(IdentityPoolId=identity_pool_id)
            identity_id = response.get('IdentityId')
            print(f"Generated identity ID: {identity_id}")
            return identity_id
        except ClientError as e:
            print(f"An error occurred while generating identity ID: {e}")
            return None
        
    def get_credentials_for_identity(self, identity_id):
        """
        Fetch temporary AWS credentials for the given identity ID.
        :param identity_id: The identity ID for which to retrieve credentials.
        :return: Temporary AWS credentials (access key, secret key, session token), or None if an error occurred.
        """
        try:
            response = self.identity_client.get_credentials_for_identity(IdentityId=identity_id)
            # Extract credentials from the response
            credentials = response.get('Credentials')
            if credentials:
                print("Fetched temporary AWS credentials successfully.")
                return credentials
            else:
                print("Failed to fetch credentials.")
                return None
        except ClientError as e:
            print(f"An error occurred while fetching credentials: {e}")
            return None

    def get_user_details(self, access_token):
        """
        Retrieve user details from Amazon Cognito using an access token.
        :param access_token: The access token obtained through user authentication.
        :return: User details, or None if an error occurred.
        """
        try:
            response = self.user_pools_client.get_user(AccessToken=access_token)
            print("Fetched user details successfully.")
            return response
        except ClientError as e:
            print(f"An error occurred while fetching user details: {e}")
            return None
        
    def update_user_attributes(self, access_token, user_attributes):
        """
        Update user attributes in Amazon Cognito.
        :param access_token: The access token obtained through user authentication.
        :param user_attributes: A list of dicts containing the user attributes to update.
        :return: None
        """
        try:
            response = self.user_pools_client.update_user_attributes(
                AccessToken=access_token,
                UserAttributes=user_attributes
            )
            print("User attributes updated successfully.")
            return response
        except ClientError as e:
            print(f"An error occurred while updating user attributes: {e}")

    def sign_up_user(self, username, password):
        """
        Attempt to sign up a user to AWS Cognito.
        
        :param username: The username of the new user.
        :param password: The password for the new user.
        :return: None. This method prints messages to indicate success or specific errors.
        """
        try:
            self.client.sign_up(
                ClientId=self.client_id,
                Username=username,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': username  # Assuming the username is the email
                    }
                ]
            )
            print(f"User {username} signed up successfully.")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UsernameExistsException':
                print(f"User {username} already exists.")
            else:
                print(f"An error occurred: {e}")

    def login(self, username, password):
        """
        Log in an existing user into Cognito User Pool.
        :param username: Username of the user.
        :param password: Password of the user.
        """
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            print(response)
            return response['AuthenticationResult']

        except ClientError as e:
            print(f"An error occurred: {e}")


