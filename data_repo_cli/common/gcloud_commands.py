import subprocess


def get_current_gcloud_user():
    auth_output = subprocess.run(['gcloud', 'auth', 'list'], capture_output=True)
    output_lines = auth_output.stdout.decode('UTF-*').strip().split('\n')
    current_user_line = list(filter(lambda line: line.startswith("*"), output_lines))
    if len(current_user_line) == 0:
        print("There is no gcloud user currently logged in. Please run `gcloud auth login` and try again")
        exit(1)
    user = current_user_line[0].split("*")[1].strip()
    return user


def get_access_token():
    token_output = subprocess.run(['gcloud', 'auth', 'print-access-token'], capture_output=True)
    access_token = token_output.stdout.decode("UTF-8").strip()
    return access_token
