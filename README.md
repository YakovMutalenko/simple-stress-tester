# Simple Stress Tester

A simple script which bombards a single URL with maximum possible number of requests.

May be used as stress testing tool. 

## Installation

1. Go to the directory where `requirements.txt` is located.
2. Create & activate Python 3 virtual environment.
3. Run in your shell:  

        pip install -r requirements.txt 

## Using

1. Make the script executable:

        $ chmod a+x tester.py
        
2. Run in your shell:

        $ ./tester.py --url http://127.0.0.1

## Notes

The script is an improved version of [Mailgun Team solution](http://blog.mailgun.com/stress-testing-http-with-twisted-python-and-treq/).

## Authors

* Eugene Zyatev ([eu@zyatev.ru](mailto:eu@zyatev.ru))
* Mailgun Team ([mailgun.com](mailto:https://www.mailgun.com/))