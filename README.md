# Test for Wordpress site and "thanks" plugin

---
## Requirements

In order to run the Selenium e2e test, you need to have the next dependencies installed:

* `python3`
* `pip3`
* `selenium` package for python3
*  Chrome driver for selenium [page](https://chromedriver.chromium.org/getting-started)
    * ``` brew install --cask chromedriver ```
    
* `selenium` package for python3.
    * ```pip3 install selenium```
    
### The Dockerfile in this repo takes care of all those dependencies.


---

## Usage

To run tests you need to set following environment variables when running your Docker Container:


**WP_URL** - URL for your local wordpress.
  * For example `-e WP_URL='http://192.168.50.2'`
  * DON'T FORGET TO ADD HTTP:// PREFIX. SELENIUM WILL THROW AN EXCEPTION WITHOUT IT.

**WP_PLUGIN_VERSION** - version of `thanks-after-post` plugin.
  * For example `-e WP_PLUGIN_VERSION=v0.10.0`

---
##Non-Headless Test
Run the test with a GUI by using:

```bash
python3 testhead.py
```
Don't forget to ```export``` or hardcode the variables in your .py file.


---
##Headless Test

Run 
```
python3 test.py
```

Or comment the next line on ```testhead.py```

```
chrome_options.add_argument("--headless")
```

In this way chrome won't be opened and the test will be able to run inside a container.

---

## Run in docker container

Build docker container:
```bash
docker build -t wp-testing .
```

And run the container with the required ENV variables. For example:
```bash
docker run --network=host --rm -it -e WP_URL='http://localhost' -e WP_PLUGIN_VERSION='v0.10.0' wp-testing
```

### DON'T FORGET TO ADD HTTP:// PREFIX. SELENIUM WILL THROW AN EXCEPTION WITHOUT IT.
