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
    # publishMode=Staging&tabTitle=adfsdfas&messageOperation=None
    body = body.split('&')
    body = list(map(lambda item: item.split('='), body))
    body = {key:value for key, value in body}
    return body
        
def parse_url_path(url_path):
    reformat = url_path.replace('%2F', '/')
    reformat = reformat.replace('+', ' ')
    return reformat    