from weblayer import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    def get(self, world):
        return u'hello {}'.format(world)
    


# map urls to request handlers using regular expressions.
mapping = [(r'/(.*)', Hello)]

# your application settings (hardcoded for this example)
config = {
    'cookie_secret': '...',
    'static_files_path': '/var/www/static',
    'template_directories': ['/my/app/templates']
}

def app_factory():
    bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
    return WSGIApplication(*bootstrapper())


def main():
    from wsgiref.simple_server import make_server
    make_server('', 8080, app_factory()).serve_forever()


if __name__ == '__main__':
    main()
