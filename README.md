# CogSpy

🔑 A straightforward utility designed to aid in testing websites that utilize AWS Cognito


<img align="right" src="cogspy.png" height="350" alt="cogpsy">

---

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  COGSPY - Spy and exploit some aws cognito missconfigurations.

  Author: rodnt

  Version: 1.1

Options:
  --help  Show this message and exit.

Commands:
  bulk-sign-up      User enumeration OR DOS Bulk sign-up users from...
  change-user-data  Command to update user data in Amazon Cognito.
  confirm           Confirm a user's account with the provided...
  get-credentials   Fetch temporary AWS credentials for a given identity ID.
  get-identity-id   Generate an identity ID for the given identity pool.
  get-user          Fetch user details from Amazon Cognito using an...
  login             Log in a user using AWS Cognito.
  register          Register a new user in AWS Cognito.
```



## Installation

Before you begin, ensure you have Python 3.6+ and pip installed on your system. Then, follow these steps to set up the CLI:

1. **Clone the Repository**

   ```bash
   git clone git@github.com:rodnt/CogSpy.git
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

python main.py get-user --access-token "<access-token>" --region "us-east-1" # get user information tokens

python3 main.py change-user-data --access-token aaaaaa --region us-east-1 # change user data ( Attack cenario, update email attribute before verification )
```

## Usage

Below are the usage instructions for each of the CLI's features:

### Bulk User Registration

- **Prepare the Files**: Create two separate files, one for usernames and one for passwords, with each entry on its own line and aligned by line number.

- **Command**:
  
  ```bash
  python main.py bulk-sign-up --client-id YOUR_CLIENT_ID --usernames-file /path/to/usernames.txt --passwords-file /path/to/passwords.txt --region YOUR_AWS_REGION
  ```

### Update User Attributes

- **Command**:
  
  Users will be prompted to enter the attribute name and new value after executing the command.
  
  ```bash
  python main.py change-user-data --access-token YOUR_ACCESS_TOKEN --region YOUR_AWS_REGION
  ```

### Fetch User Details

- **Command**:
  
  ```bash
  python main.py get-user --access-token YOUR_ACCESS_TOKEN --region YOUR_AWS_REGION
  ```

### Get Temporary AWS Credentials

- **Command**:
  
  ```bash
  python main.py get-credentials --identity-id YOUR_IDENTITY_ID --region YOUR_AWS_REGION
  ```
### Finding endpoints with others tools like httpx and katana from [https://github.com/projectdiscovery](https://github.com/projectdiscovery)

```bash
# grep pools
httpx -l urls.txt -mr '(af-south-1|ap-east-1|ap-northeast-[123]|ap-south-[12]|ap-southeast-[1234]|ca-central-1|ca-west-1|cn-north-[1]|cn-northwest-1|eu-central-[12]|eu-north-1|eu-south-[12]|eu-west-[123]|il-central-1|me-central-1|me-south-1|sa-east-1|us-east-[12]|us-gov-east-1|us-gov-west-1|us-west-[12])_[a-zA-Z0-9]+'

# identity pools
httpx -l urls.txt -mr '(af-south-1|ap-east-1|ap-northeast-[123]|ap-south-[12]|ap-southeast-[1234]|ca-central-1|ca-west-1|cn-north-1|cn-northwest-1|eu-central-[12]|eu-north-1|eu-south-[12]|eu-west-[123]|il-central-1|me-central-1|me-south-1|sa-east-1|us-east-[12]|us-gov-east-1|us-gov-west-1|us-west-[12]):[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
```

## Possibile Fixing/Mitigations
- Attribute permissions and scopes
  - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html
- Confidential client
  - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html
- Tutorial: Using lambda + AWS Cognito triggers to Only Allow Auto-Verification to specific domain
  - https://medium.com/@earlg3/using-lambda-aws-cognito-triggers-to-only-allow-auto-verification-to-specific-domain-db2efea79c44


## Additional Information

- **Customizing the CLI**: This CLI can be extended or customized to include more features from AWS Cognito.

## License

Apache 2 License.. 

## Contributing

Instructions for how contributors can report issues or contribute to the project.

---
