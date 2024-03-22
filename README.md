# CogSpy

<img align="right" src="cogspy.png" height="350" alt="cogpsy">

🔑 A straightforward utility designed to aid in testing websites that utilize AWS Cognito

---

```bash
Usage: main.py [OPTIONS] COMMAND [ARGS]...
  COGSPY - Spy and exploit some aws cognito missconfigurations.
  Author: rodnt
  Version: 1.1

Options:
  --help  Show this message and exit.

Commands:
  bulk-sign-up      User enumeration OR DOS (block new users access) -...
  change-user-data  Command to update user data in Amazon Cognito.
  confirm           Confirm a user's account with the provided...
  get-credentials   Fetch temporary AWS credentials for a given identity ID.
  get-identity-id   Generate an identity ID for the given identity pool.
  get-user          Fetch user details from Amazon Cognito using an...
  register          Register a new user in AWS Cognito.

```



## Installation

Before you begin, ensure you have Python 3.6+ and pip installed on your system. Then, follow these steps to set up the CLI:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/rodnt/cogspy.git
   cd cogspy
   ```

2. **Create and Activate a Virtual Environment (Optional but Recommended)**

   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

### TL;DR commands

```bash
python3 main.py confirm --username boto --confirmation-code 429258 --region us-east-1 --client-id 4t1231db5asd3jcrco5 # confirm user creation

python3 main.py register --username boto --email aaaaaa@maildrop.cc  --password Pentest --region us-east-1 --client-id 4tl12o1sa121125121212 # create user

python3 main.py get-identity-id --region us-east-1 --identity-id us-east-1:123111-0730-4829-9ee0-g123fs1a # get identity id

python3 main.py get-credentials --identity-id us-east-1:123111-0730-4829-9ee0-g123fs1a --region "us-east-1" # get temporary credentials

python main.py get_user --access-token "<access-token>" --region "us-east-1" # get user information tokens

python3 main.py change-user-data --access-token aaaaaa --region us-east-1 # change user data ( Attack cenario, update email attribute before verification )
```



## Usage

Below are the usage instructions for each of the CLI's features:

### Bulk User Registration

- **Prepare the Files**: Create two separate files, one for usernames and one for passwords, with each entry on its own line and aligned by line number.

- **Command**:
  
  ```bash
  python main.py bulk_sign_up --client-id YOUR_CLIENT_ID --usernames-file /path/to/usernames.txt --passwords-file /path/to/passwords.txt --region YOUR_AWS_REGION
  ```

### Update User Attributes

- **Command**:
  
  Users will be prompted to enter the attribute name and new value after executing the command.
  
  ```bash
  python main.py change_user_data --access-token YOUR_ACCESS_TOKEN --region YOUR_AWS_REGION
  ```

### Fetch User Details

- **Command**:
  
  ```bash
  python main.py get_user --access-token YOUR_ACCESS_TOKEN --region YOUR_AWS_REGION
  ```

### Get Temporary AWS Credentials

- **Command**:
  
  ```bash
  python main.py get_credentials --identity-id YOUR_IDENTITY_ID --region YOUR_AWS_REGION
  ```

## Additional Information

- **Customizing the CLI**: This CLI can be extended or customized to include more features from AWS Cognito.
- **Security**: Always ensure your usernames and passwords are handled securely. Avoid storing sensitive information in plaintext.

## License

Include license information here.

## Contributing

Instructions for how contributors can report issues or contribute to the project.

---
