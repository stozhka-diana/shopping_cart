# Shopping cart API
[![Testing](https://github.com/BorisPlaton/shopping_cart_api/actions/workflows/testing.yml/badge.svg)](https://github.com/BorisPlaton/shopping_cart_api/actions/workflows/testing.yml)

[Implementation](https://docs.google.com/document/d/16M_jtHkbrHgI_gUj9vq6p_uIQVQTFuW2kXUsK-S4RSk/edit) of the API of a shopping cart, products and their categories.

The API [documentation](https://documenter.getpostman.com/view/25786085/2s9YywdeQC) via Postman.

## Setup

### Development

#### .env.dist

All environment variables that are used in development are specified in the `.env.dist` file. This file is used in the `docker-compose.dev.yml` file and shell scripts. 

#### Virtual environment

Firstly, you must install all necessary dependencies. For this, you should create a virtual environment. For instance, you may use a `virtualenv`:
```
$ virtualenv --python 3.10 venv
```
Afterwards, activate it:
```
$ . venv/bin/activate
```
Two `requirements` file exist:
* `requirements.dev.txt` - contains all dependencies that are used during a development process
* `requirements.txt` - contains all dependencies that are used at the production

Install all packages that are specified in the `requirements.dev.txt` file. Run the following command to make it:
```
$ pip install -r requirements/dev.txt
```

### Production

#### .env
Before starting the application, you must create `.env` in the root folder. You already have a `.env.prod` file, which contains the template of the `.env` file and some default values.

#### Start application

You have a `docker-compose.yml` file in the root directory with all necessarily configuration. If you have created the `.env` file, you will start the application if you print following command:
```
$ docker-compose up
```
The application works on `8888` port at the `127.0.0.1` IP address.
