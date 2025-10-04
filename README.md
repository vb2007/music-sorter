# A simple music sorter made with Python

A script, that runs through a specified folder's songs, then puts them into their album's folders.

It's made to be used with [spotyDL](https://github.com/spotDL/spotify-downloader).

## Usage

### Generally on Windows

Install dependencies with `pip`:

```shell
pip install -r requirements.txt
```

Then run the script:

```shell
python main.py
```

### Using venv

#### Install required packages using your package manager

Using apt:

```shell
sudo apt install python3.11 python3.11-venv pip
```

Using pacman:

```shell
sudo pacman -S python3
```

#### Create & use a venv

Creating a venv:

```shell
python3 -m venv music-sorter
```

Activating the venv:

```shell
source music-sorter/bin/activate
```

Installing dependencies:

```shell
pip install -r requirements.txt
```

Running the script:

```shell
python3 main.py:
```

Deactivating the venv (when done):

```shell
deactivate
```
