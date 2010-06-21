
`thruflo.webapp` is a WSGI compatible web application framework.  

It's poor quality, untested and no doubt deeply flawed.  But is it just the way *I* want my webapp framework to be:

* `re.compile` based url mapping
* classes for `RequestHandler`s with methods that correspond to the HTTP Request's method, e.g.: `def post(self)` handles a `POST` request
* a `webob.Request` as self.request
* `return foo` as the method of responding, where `foo` can be a webob.Response, a string or either a list or a dictionary (to return `json`)
* `mako` templates with builtin methods including `static_url`, `xsrf_form_html` and `escape` to the template, as well as references to `handler` and `request`

Or to put it another way:

    from thruflo.webapp import web
    
    class Hello(web.RequestHandler):
        def get(self):
            return 'hello world'
            
        
    
    mapping = [('/.*', MainPage)]
    application = web.WSGIApplication(mapping)
    

Or see `thruflo.webapp.demo`.