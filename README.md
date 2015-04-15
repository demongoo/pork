# Pork: Simple message storage
------------------------------

Application is intended as temporary storage for output from a restricted system, where you somehow can 
execute command but cannot see direct output (yes, this happens!).

### Deployment
 
App is simple Flask application for `python 2.7`, can be deployed in one of two ways:

* on any server, install deps in `requirements.txt`, then `python pork.py $PORT`
* ready for Heroku deployment

### Usage

Just post any content to `/` using HTTP POST, and see it using HTTP GET.

For example, linux command line usage:

    ps aux |  curl --data-binary @- http://your.app.url