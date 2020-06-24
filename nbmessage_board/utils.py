import urllib.parse

def load_yaml(path):
    import yaml
    try:
        with open(path, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return data
    except FileNotFoundError:
        raise FileNotFoundError('could not load yaml at path: {path}')
    except Exception as e:
        raise e
    
def parse_body(body):
    body = urllib.parse.parse_qs(body)
    
    for k, v in body.items():
        if len(v) == 1:
            body.update({k: v[0]})
    return body

def unquote_plus(text):
    return urllib.parse.unquote_plus(text)

def parse_url_path(url_path):
    reformat = url_path.replace('%2F', '/')
    reformat = reformat.replace('+', ' ')
    return reformat    