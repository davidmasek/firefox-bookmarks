import json
from typing import Optional
import uuid
import argparse
import sys
import requests
from pathlib import Path
import base64

parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True, type=Path, help='JSON file with bookmarks.')

args = parser.parse_args()

MAX_FILENAME_LEN = 200

icons_dir = Path('icons')
icons_dir.mkdir(exist_ok=True)

def get_favicon(url: str) -> Optional[str]:
    # empty urls are not valid
    if not url:
        return None
    # standardize some URIs used by Firefox
    if url.startswith('fake-favicon-uri:'):
        url = url.replace('fake-favicon-uri:', '', 1)

    # deal with directly embedded image data 
    if url.startswith('data:image'):
        print('data:image currently not supported', file=sys.stderr)
        return None
    
    # filter unsupported URIs (it still may be a valid URI but currently unsupporetd)
    if not url.startswith('http'):
        print(f'unexpected url: {url}', file=sys.stderr)
        return None
    
    # convert url to valid filename with base64
    file_name = base64.urlsafe_b64encode(url.encode('utf8')).decode('utf8')
    if len(file_name) > MAX_FILENAME_LEN:
        print(f'url {url} too long, cropping resulting filename', file=sys.stderr)
        file_name = file_name[:MAX_FILENAME_LEN]

    file_path = icons_dir / file_name
    # don't re-download files (OK enough solution, doesn't deal with resource updates)
    if file_path.exists():
        return file_path

    try:
        with requests.get(url) as response:
            if response.status_code == 200:
                # encode to valid filename
                with open(file_path, 'wb') as fh:
                    fh.write(response.content)
                return file_path
            # else:
            #     print(f'failed to download {url}, status={response.status_code}', file=sys.stderr)
    except requests.exceptions.ConnectionError as ex:
        print(f'cannot connect to {url}: {ex}', file=sys.stderr)

    return None

def traverse(node):
    title = node.get('title', '')

    uri = node.get('uri', '')
    iconuri = node.get('iconuri', '')
    iconpath = get_favicon(iconuri)

    has_children = 'children' in node and len(node['children']) > 0

    guid = node['guid']
    body_id = uuid.uuid4()
    if has_children:
        print(f'''
        <div class="card">
            <div class="card-header">
                <h2><a 
                    data-guid={guid}
                    class="btn btn-link tree-node" 
                    data-toggle="collapse" 
                    href="#{body_id}" 
                    role="button" 
                >
                    {title}
                </a></h2>
            </div>
            <div class="collapse" id="{body_id}">
                <div class="card-body">
                    <ul>
        '''
        )
        for ch in node['children']:
            traverse(ch)
        print('''
                    </ul>
                </div>
            </div>
        </div>
        ''')
    else:
        img = ''
        if iconpath:
            img = f'<img src="{iconpath}">'

        print(f'''
        <li>
            {img}
            <a 
                class="tree-node"
                data-guid={guid}
                href="{uri}"
                target="_blank"
            >{title}</a>
        </li>
        ''')



def start_traverse(root):
    print('''<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Bookmarks</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.15.4/css/fontawesome.min.css" integrity="sha384-jLKHWM3JRmfMU0A5x5AkjWkw/EYfGUAGagvnfryNV3F9VqM98XiIH7VBGVoxVSc7" crossorigin="anonymous">
        <link rel="stylesheet" href="main.css">
    </head>
    <body>
        <div class="card">
            <div class="card-header">
                <h2><a 
                    data-toggle="collapse" 
                    href="#export-data-container" 
                    role="button"
                >Export Data
                </a></h2>
                <button type="button" class="btn btn-primary btn-sm" id="export">Export</button>
            </div>
            <div class="collapse" id="export-data-container">
                <div class="card-body" id="export-data">
                </div>
            </div>
        <div>
    ''')
    

    title = root['title']
    if title: f'<h1>{title}</h1>'
    if 'children' in root:
        children = root['children']
    else:
        children = []
    for ch in children:
        traverse(ch)
    
    print('''</div>
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <script src="main.js"></script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    with open(args.data) as fh:
        data = json.load(fh)

    start_traverse(data)
