#!/usr/bin/env python
from app import api

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000, debug=True)
