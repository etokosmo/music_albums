# Display Music Album Service

## About

Service for displaying the album, artist and tracks.

The main idea is to serialize according to a given template and sort by fields.

<details>
  <summary>Example of template</summary>

```json
[
  {
    "album": "album1[2022]",
    "name": "album1",
    "artist@name": "artist_name1",
    "tracks": [
      "track1",
      "track2",
      "track3"
    ]
  },
  ...
]
```

</details>

## Website example

![Albums](https://user-images.githubusercontent.com/93794917/199439438-274d9bd8-ed37-4b32-8ee7-0a69e0815fb9.gif)

## API

You can send POST request to load album in db to `http://<YOUR_DOMEN>/api/`.

<details>
  <summary>Example</summary>

URL: `http://127.0.0.1:8000/api/`

HEADERS: `'Content-Type': 'application/json'`

JSON:

```json
  {
  "album": "The Dark Side Of The Moon[1973]",
  "name": "The Dark Side Of The Moon",
  "artist@name": "Pink Floyd",
  "tracks": [
    "Speak to Me",
    "Breathe",
    "On the Run",
    "Time",
    "The Great Gig in the Sky"
  ]
}
```

</details>

You can send GET request to get all albums in db to `http://<YOUR_DOMEN>/api/`.

<details>
  <summary>Example</summary>

URL: `http://127.0.0.1:8000/api/`

</details>

You can send GET request to get all albums in db with ordering
to `http://<YOUR_DOMEN>/api/sort/?ordering=name`.

Order by `name`, `-name`, `artist`, `-artist`

<details>
  <summary>Example</summary>

URL: `http://<YOUR_DOMEN>/api/sort/?ordering=name`

</details>

## Management command

You can populate the database with test data to test the service.

* `python manage.py load_album` - Load albums from `albums.json` to db with
  API. You need start your server before.

## Configurations

* Python version: 3.10
* Libraries: [requirements.txt](https://github.com/etokosmo/music_albums/blob/main/requirements.txt)

## Launch

### Local server

- Download code
- Through the console in the directory with the code, install the virtual
  environment with the command:

```bash
python3 -m venv env
```

- Activate the virtual environment with the command:

```bash
source env/bin/activate
```

- Install the libraries with the command:

```bash
pip install -r requirements.txt
```

- Write the environment variables in the `.env` file in the format KEY=VALUE

`SECRET_KEY` - A secret key for a particular Django installation. This is used
to provide cryptographic signing, and should be set to a unique, unpredictable
value.

`ALLOWED_HOSTS` - A list of strings representing the host/domain names that
this Django site can serve. This is a security measure to prevent HTTP Host
header attacks, which are possible even under many seemingly-safe web server
configurations.

`DEBUG` - A boolean that turns on/off debug mode. If your app raises an
exception when DEBUG is True, Django will display a detailed traceback,
including a lot of metadata about your environment, such as all the currently
defined Django settings (from settings.py).

`DATABASE_URL` - URL to db. For more information
check [this](https://github.com/jazzband/dj-database-url).

P.S. Default values are already set

- Create your database with the command:

```bash
python manage.py makemigrations
python manage.py migrate
```

- Run local server with the command (it will be available
  at http://127.0.0.1:8000/):

```bash
python manage.py runserver
```
