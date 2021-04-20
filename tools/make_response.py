from flask import redirect as f_redirect

HOST = 'http://127.0.0.1:8080/'


def redirect(name, **kwargs):
    requests = [str(x) + '=' + kwargs[x] for x in kwargs.keys()]
    request_line = '?' + '&'.join(requests)
    if not kwargs:
        return f_redirect(HOST + name)
    return f_redirect(HOST + name + request_line)
