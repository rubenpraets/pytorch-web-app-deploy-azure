# Initial build setup

Let us have a separate virtual environment for our development.

```sh
$ sudo apt install python3-venv
$ python3 -m venv webappenv
$ source ./webapp/bin/activate
```

Clone the repo and install the dependencies.

```sh
$ git clone https://github.com/bigvisionai/pytorch-web-app-deploy-azure
$ cd pytorch-web-app-deploy-azure
$ pip install -r requirements.txt
```
