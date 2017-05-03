#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)

@app.route('/')
def show_login():
    return 'Login'
    
    
if __name__ == "__main__":
    app.run()