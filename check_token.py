import os

token = os.getenv('GITHUB_TOKEN')
if token:
    print(f"Token is set. First 4 characters: {token[:4]}")
else:
    print("Token is not set.")