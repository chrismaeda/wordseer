#!/usr/bin/env python

"""
Run the wordseer_flask website.
"""
import sys
hostname = '127.0.0.1'
portnum = 80
if len(sys.argv)>1:
    hostname = sys.argv[1]
if len(sys.argv)>2:
    portnum = sys.argv[2]
from app import app



if __name__ == '__main__':
#    app.debug = True
    
    app.run(host=hostname, port=portnum, debug=True)
