import json
import uuid
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True, type=Path, help='JSON file with bookmarks.')

args = parser.parse_args()

with open(args.data) as fh:
    data = json.load(fh)

def traverse(node):
    title = node.get('title', '')

    uri = node.get('uri', '')
    iconuri = ''
    # iconuri = node.get('iconuri', '')
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
        if iconuri:
            img = f'<img src="{iconuri}" width=16 height=16>'

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
    start_traverse(data)
