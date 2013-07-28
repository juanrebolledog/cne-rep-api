from libs import app
import cStringIO
import gzip
from flask import request


@app.after_request
def compress(response):
    accept_encoding = request.headers.get('Accept-Encoding', '')

    if 'gzip' not in accept_encoding.lower():
        return response

    if response.status_code != 200 or len(response.data) < 500 \
    or 'Content-Encoding' in response.headers:
        return response

    compress_level = 6
    gzip_buffer = cStringIO.StringIO()
    gzip_file = gzip.GzipFile(mode='wb', \
    compresslevel=compress_level, fileobj=gzip_buffer)
    gzip_file.write(response.data)
    gzip_file.close()
    response.data = gzip_buffer.getvalue()
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = str(len(response.data))
    return response

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')