# Firefox Bookmarks Browser

Utility for browsing Firefox bookmarks. Generates interactive `html` page from exported bookmarks for more comfortable browsing.

Currently only browsing is fully supported. Other features (deleting/editing) might be added in the future.

## Usage

1. Export ("backup") bookmarks

Bookmarks -> Manage Bookmarks -> Import and Backup -> Backup -> Save (filename for example `bookmarks-2021-11-07.json`)

2. Generate HMTL

```bash
python3 main.py --data 'bookmarks-2021-11-07.json' > index.html
```

3. Open HTML file

## Requirements

Python 3.6+ is required. Only standard libraries are used. App was tested with Firefox 94 (but will probably work on a large range of versions).

## Progress

- [x] generate HMTL from JSON export
- [x] make HMTL interactive (section collapsing) 
- [x] allow item selection (and GUID export)
- [ ] remove selected bookmarks and generate new JSON file

## Credits

This utility uses [Bootstrap](https://getbootstrap.com/) and [Font Awesome](https://fontawesome.com/).