# Test for Wordpress site and "thanks" plugin

## Requirements

* `python3`
* `pip3`
* `selenium` package for python3
* Chrome driver for selenium

## Setup

Install `selenium` package for python3.
```bash
pip3 install selenium
```

Install Chrome driver for selenium. Check out [page](https://chromedriver.chromium.org/getting-started).

## Usage

To run tests you need to set following environment variables:

**WP_URL** - URL for your local wordpress. For example `export WP_URL='http://192.168.50.2'`
**WP_PLUGIN_VERSION** - version of `thanks-after-post` plugin. For example `export WP_PLUGIN_VERSION=v0.10.0`

Run command:
```bash
python3 test.py
```

This will open new Chrome browser window and run all the tests.

## Test in non-interactive mode

First of all comment line:
```
    chrome_options.add_argument("--headless")
```

So your browser wouln't be opened. It's needed to run it in container.

## Run in docker container

After you apply changes from previous paragraph you should build docker container:
```bash
docker built -t wp-testing .
```

Next time you need to run docker container with provided variables. For example in testing of wordpress that was setup in VM:
```bash
docker run --network=host --rm -it -e WP_URL='http://192.168.50.2' -e WP_PLUGIN_VERSION='v0.10.0' wp-testing
```
