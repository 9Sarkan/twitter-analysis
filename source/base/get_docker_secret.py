import os

root = os.path.abspath(os.sep)


def get_docker_secret(name, default=None, secrets_dir=os.path.join(root, 'run', 'secrets')):
    # initiallize value
    value = None

    # try to read from secret file
    try:
        with open(os.path.join(secrets_dir, name), 'r') as secret_file:
            value = secret_file.read().strip()
    except IOError:
        return default

    return value
