#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for `thruflo.webapp.request`.
"""

import unittest
from mock import Mock

def _was_called_with(m, *args, **kwargs):
    """ Takes a mock and the args and kwargs it should have been
      called with, iterates through the call_args_list and returns
      `True` if they match once.
      
          >>> m = Mock()
          >>> m1 = m('a', foo='bar')
          >>> m2 = m('b', baz='blah')
          >>> _was_called_with(m, 'b', baz='blah')
          True
          >>> _was_called_with(m, 'a', foo='bar')
          True
          >>> _was_called_with(m, 'a')
          False
          >>> _was_called_with(m, baz='blah')
          False
      
    """
    
    for item in m.call_args_list:
        if item[0] == args and item[1] == kwargs:
            return True
        
    return False
    


class TestInitHandler(unittest.TestCase):
    """ Test the logic of `Handler.__init__`.
    """
    
    def _make_one(self, *args, **kwargs):
        from thruflo.webapp.request import Handler
        return Handler(*args, **kwargs)
        
    
    def setUp(self):
        """ Monkey patch the component registry.
        """
        
        self.adapter = Mock()
        self.adapter.return_value = 'adapted'
        self.mock_registry = Mock()
        self.mock_registry.getUtility = Mock()
        self.mock_registry.getUtility.return_value = 'utility'
        self.mock_registry.getAdapter = Mock()
        self.mock_registry.getAdapter.return_value = 'adapted from registry'
        
        import thruflo.webapp.request
        thruflo.webapp.request.registry = self.mock_registry
        
    
    def test_requires_args(self):
        """ Must pass in `request`, `response` and `settings`.
        """
        
        self.assertRaises(
            TypeError,
            self._make_one
        )
        self.assertRaises(
            TypeError,
            self._make_one,
            ''
        )
        self.assertRaises(
            TypeError,
            self._make_one,
            '',
            ''
        )
        
    
    def test_adapts_request(self):
        """ `request` is available as `self.request`.
        """
        
        handler = self._make_one('req', '', '')
        self.assertTrue(handler.request == 'req')
        
    
    def test_adapts_response(self):
        """ `response` is available as `self.response`.
        """
        
        handler = self._make_one('', 'resp', '')
        self.assertTrue(handler.response == 'resp')
        
    
    def test_adapts_settings(self):
        """ `settings` is available as self.settings`.
        """
        
        handler = self._make_one('', '', 'settings')
        self.assertTrue(handler.settings == 'settings')
        
    
    def test_template_renderer_adapter(self):
        """ If `template_renderer_adapter` is not None, it's called with
          `self.settings` and the return value is available as 
          `self.template_renderer`.
        """
        
        handler = self._make_one(
            '', 
            '', 
            '',
            template_renderer_adapter=self.adapter
        )
        self.adapter.assert_called_with(handler.settings)
        self.assertTrue(handler.template_renderer == 'adapted')
        
    
    def test_template_renderer_adapter_from_registry(self):
        """ If `template_renderer` is None, which is the default, 
          `self.template_renderer` is looked up via the component registry.
        """
        
        from thruflo.webapp.interfaces import ITemplateRenderer
        
        handler = self._make_one('', '', '')
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter, 
                '',
                ITemplateRenderer
            )
        )
        self.assertTrue(handler.template_renderer == 'adapted from registry')
        
        handler = self._make_one(
            '', 
            '', 
            '', 
            template_renderer_adapter=None
        )
        self.assertTrue(handler.template_renderer == 'adapted from registry')
        
    
    def test_authentication_manager_adapter(self):
        """ If `authentication_manager_adapter` is not None, it's called
          with `self.request` and the return value is available as `self.auth`.
        """
        
        handler = self._make_one(
            '', 
            '', 
            '',
            authentication_manager_adapter=self.adapter
        )
        self.adapter.assert_called_with(handler.request)
        self.assertTrue(handler.auth == 'adapted')
        
    
    def test_authentication_manager_adapter_from_registry(self):
        """ If `authentication_manager_adapter` is None, which is the default,
          `self.auth` is looked up via the component registry.
        """
        
        from thruflo.webapp.interfaces import IAuthenticationManager
        
        handler = self._make_one('', '', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler.request,
                IAuthenticationManager
            )
        )
        self.assertTrue(handler.auth == 'adapted from registry')
        
        handler = self._make_one(
            '', 
            '', 
            '', 
            authentication_manager_adapter=None
        )
        self.assertTrue(handler.auth == 'adapted from registry')
        
    
    def test_secure_cookie_wrapper_adapter(self):
        """ If `secure_cookie_wrapper_adapter` is not None, it's called
          with `self` and the return value is available as `self.cookies`.
        """
        
        handler = self._make_one(
            '', 
            '', 
            '', 
            secure_cookie_wrapper_adapter=self.adapter
        )
        self.adapter.assert_called_with(
            handler.request, 
            handler.response, 
            handler.settings
        )
        self.assertTrue(handler.cookies == 'adapted')
        
    
    def test_secure_cookie_wrapper_adapter_from_registry(self):
        """ If `secure_cookie_wrapper_adapter` is None, which is the default,
          `self.cookies` is looked up via the component registry.
        """
        
        from thruflo.webapp.interfaces import ISecureCookieWrapper
        
        handler = self._make_one('', '', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler.request, 
                handler.response, 
                handler.settings,
                ISecureCookieWrapper
            )
        )
        self.assertTrue(handler.cookies == 'adapted from registry')
        
        handler = self._make_one(
            '', 
            '', 
            '', 
            secure_cookie_wrapper_adapter=None
        )
        self.assertTrue(handler.cookies == 'adapted from registry')
        
    
    def test_method_selector_adapter(self):
        """ If `method_selector_adapter` is not None, it's called with `self`
          and the return value is available as `self._method_selector`.
        """
        
        handler = self._make_one(
            '', 
            '', 
            '', 
            method_selector_adapter=self.adapter
        )
        self.adapter.assert_called_with(handler)
        self.assertTrue(handler._method_selector == 'adapted')
        
    
    def test_method_selector_adapter_from_registry(self):
        """ If `method_selector_adapter` is None, which is the default,
          `self.auth` is looked up via the component registry.
        """
        
        from thruflo.webapp.interfaces import IMethodSelector
        
        handler = self._make_one('', '', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler,
                IMethodSelector
            )
        )
        self.assertTrue(handler._method_selector == 'adapted from registry')
        
        handler = self._make_one(
            '', 
            '', 
            '', 
            method_selector_adapter=None
        )
        self.assertTrue(handler._method_selector == 'adapted from registry')
        
    
    def test_response_normaliser_adapter(self):
        """ `response_normaliser_adapter` defaults to None and is available
          as `self.response_normaliser_adapter`.
        """
        
        handler = self._make_one('', '', '')
        self.assertTrue(handler._response_normaliser_adapter is None)
        
        handler = self._make_one(
            '', 
            '', 
            '', 
            response_normaliser_adapter=42
        )
        self.assertTrue(handler._response_normaliser_adapter == 42)
        
    
    

class TestHandlerGetArguments(unittest.TestCase):
    """ Test the logic of `handler.get_argument` and 
      `handler.get_arguments`.
    """
    
    def _make_one(self, *args, **kwargs):
        from thruflo.webapp.request import Handler
        return Handler(*args, **kwargs)
        
    
    def setUp(self):
        self.request = Mock()
        self.response = Mock()
        self.settings = {}
        self.template_renderer_adapter = Mock()
        self.static_url_generator_adapter = Mock()
        self.authentication_manager_adapter = Mock()
        self.secure_cookie_wrapper_adapter = Mock()
        self.method_selector_adapter = Mock()
        self.handler = self._make_one(
            self.request,
            self.response,
            self.settings,
            template_renderer_adapter=self.template_renderer_adapter,
            static_url_generator_adapter=self.static_url_generator_adapter,
            authentication_manager_adapter=self.authentication_manager_adapter,
            secure_cookie_wrapper_adapter=self.secure_cookie_wrapper_adapter,
            method_selector_adapter=self.method_selector_adapter
        )
        
    
    def test_get_argument_calls_get_arguments(self):
        """ `get_argument` calls `get_arguments` with `strip` defaulting to
          `False`.
        """
        
        self.handler.get_arguments = Mock()
        self.handler.get_arguments.return_value = []
        self.handler.get_argument('foo')
        self.handler.get_arguments.assert_called_with('foo', strip=False)
        
    
    def test_get_argument_strip(self):
        """ `strip` is passed through.
        """
        
        self.handler.get_arguments = Mock()
        self.handler.get_arguments.return_value = []
        self.handler.get_argument('foo', strip=True)
        self.handler.get_arguments.assert_called_with('foo', strip=True)
        
    
    def test_get_argument_return_value(self):
        """ `get_argument` returns the last item from the list `get_arguments`
          returns.
        """
        
        self.handler.get_arguments = Mock()
        self.handler.get_arguments.return_value = ['a', 'b']
        self.assertTrue(self.handler.get_argument('foo') == 'b')
        
    
    def test_get_argument_default(self):
        """ Unless get_arguments returns `[]` in which case `get_argument`
          returns `default` which defaults to `None`.
        """
        
        self.handler.get_arguments = Mock()
        self.handler.get_arguments.return_value = []
        self.assertTrue(self.handler.get_argument('foo') is None)
        self.assertTrue(
            self.handler.get_argument('foo', default='abc') == 'abc'
        )
        
    
    def test_get_arguments_calls_get_arguments(self):
        """ `get_argument` calls `request.params.get`.
        """
        
        self.handler.get_arguments('foo')
        self.request.params.get.assert_called_with('foo', [])
        
    
    def test_get_arguments_calls_wraps_single_value(self):
        """ If `request.params.get` returns a single value, wraps it in 
          a `list`.
        """
        
        self.request.params.get.return_value = 'a'
        self.assertTrue(self.handler.get_arguments('foo') == ['a'])
        
    
    def test_get_arguments_calls_multiple_value(self):
        """ If `request.params.get` returns a list, returns it.
        """
        
        self.request.params.get.return_value = ['a', 'b']
        self.assertTrue(self.handler.get_arguments('foo') == ['a', 'b'])
        
    
    def test_get_arguments_doesnt_strip(self):
        """ Doesn't strip by default.
        """
        
        self.request.params.get.return_value = [' a ', ' b ']
        self.assertTrue(self.handler.get_arguments('foo') == [' a ', ' b '])
        
    
    def test_get_arguments_unless_told_to_strip(self):
        """ Strips if told to.
        """
        
        self.request.params.get.return_value = [' a ', ' b ']
        self.assertTrue(
            self.handler.get_arguments('foo', strip=True) == ['a', 'b']
        )
        
    
    

class TestHandlerXSRF(unittest.TestCase):
    """ Test the logic of `handler.xsrf_token`, `handler.xsrf_input` 
      and `.xsrf_validate`.
    """
    
    def _make_one(self, *args, **kwargs):
        from thruflo.webapp.request import Handler
        return Handler(*args, **kwargs)
        
    
    def setUp(self):
        self.request = Mock()
        self.response = Mock()
        self.settings = {}
        self.template_renderer_adapter = Mock()
        self.static_url_generator_adapter = Mock()
        self.authentication_manager_adapter = Mock()
        self.secure_cookie_wrapper_adapter = Mock()
        self.method_selector_adapter = Mock()
        self.handler = self._make_one(
            self.request,
            self.response,
            self.settings,
            template_renderer_adapter=self.template_renderer_adapter,
            static_url_generator_adapter=self.static_url_generator_adapter,
            authentication_manager_adapter=self.authentication_manager_adapter,
            secure_cookie_wrapper_adapter=self.secure_cookie_wrapper_adapter,
            method_selector_adapter=self.method_selector_adapter
        )
        
    
    def test_xsrf_token_returns__xsrf_token(self):
        """ If `self._xsrf_token` then return it.
        """
        
        self.handler._xsrf_token = 'foobar'
        self.assertTrue(self.handler.xsrf_token == 'foobar')
        
    
    def test_xsrf_token_tries_cookies(self):
        """ Otherwise first tries `self.cookies`.
        """
        
        self.handler.cookies.get.return_value = 'something'
        self.assertTrue(self.handler.xsrf_token == 'something')
        self.handler.cookies.get.assert_called_with('_xsrf')
        
    
    def test_xsrf_token_generate(self):
        """ Then generates a new token and sets it as the cookie value
          and caches it as self._xsrf_token.
        """
        
        import thruflo.webapp.request
        
        generate_hash = Mock()
        generate_hash.return_value = 'digest'
        thruflo.webapp.request.generate_hash = generate_hash
        
        self.handler.cookies.get.return_value = None
        self.assertTrue(self.handler.xsrf_token == 'digest')
        generate_hash.assert_called_with()
        
        self.handler.cookies.set.assert_called_with(
            '_xsrf',
            'digest',
            expires_days=None
        )
        
        self.assertTrue(self.handler._xsrf_token == 'digest')
    
    def test_xsrf_input_returns__xsrf_input(self):
        """ If `self._xsrf_input` then return it.
        """
        
        self.handler._xsrf_input = '<input />'
        self.assertTrue(self.handler.xsrf_input == '<input />')
        
    
    def test_xsrf_input_tag_from_token(self):
        """ Return input tag with escaped `self.xsrf_token` as value
          and cache it as self._xsrf_input.
        """
        
        import thruflo.webapp.request
        __xhtml_escape = thruflo.webapp.request
        
        xhtml_escape = Mock()
        xhtml_escape.return_value = 'digest &amp; sons'
        thruflo.webapp.request.xhtml_escape = xhtml_escape
        self.handler._xsrf_token = 'digest & sons'
        self.assertTrue(
            self.handler.xsrf_input == 
            u'<input type="hidden" name="_xsrf" value="digest &amp; sons" />'
        )
        xhtml_escape.assert_called_with('digest & sons')
        
        thruflo.webapp.request.xhtml_escape = __xhtml_escape
        
    
    def test_xsrf_validate_method_not_post_returns_none(self):
        """ No need to validate unless the request is a POST.
        """
        
        self.handler.request.method = 'notpost'
        self.assertTrue(self.handler.xsrf_validate() is None)
        
    
    def test_xsrf_validate_xmlhttprequest_returns_none(self):
        """ No need to validate if it's an XMLHttpRequest.
        """
        
        self.handler.request.method = 'post'
        self.handler.request.headers.get.return_value = 'XMLHttpRequest'
        self.assertTrue(self.handler.xsrf_validate() is None)
        self.handler.request.headers.get.assert_called_with('X-Requested-With')
        
    
    def test_xsrf_validate_raise_error_if_no_token_in_request(self):
        """ Raise error if we haven't got an xsrf token in the request.
        """
        
        from thruflo.webapp.request import XSRFError
        
        self.handler.request.method = 'post'
        self.handler.request.headers.get.return_value = 'NotAnXMLHttpRequest'
        self.handler.get_argument = Mock()
        self.handler.get_argument.return_value = None
        self.assertRaises(
            XSRFError,
            self.handler.xsrf_validate
        )
        self.handler.get_argument.assert_called_with('_xsrf', None)
        
    
    def test_xsrf_validate_raise_error_if_token_doesnt_match(self):
        """ Raise error the token in the request doesn't match 
          `self.xsrf_token`.
        """
        
        from thruflo.webapp.request import XSRFError
        
        self.handler.request.method = 'post'
        self.handler.request.headers.get.return_value = 'NotAnXMLHttpRequest'
        self.handler.get_argument = Mock()
        self.handler.get_argument.return_value = 'foo'
        self.handler._xsrf_token = 'bar'
        self.assertRaises(
            XSRFError,
            self.handler.xsrf_validate
        )
        
    
    def test_xsrf_validate_success(self):
        """ Pass silently if the token in the request does match 
          `self.xsrf_token`.
        """
        
        self.handler.request.method = 'post'
        self.handler.request.headers.get.return_value = 'NotAnXMLHttpRequest'
        self.handler.get_argument = Mock()
        self.handler.get_argument.return_value = 'matches'
        self.handler._xsrf_token = 'matches'
        self.assertTrue(self.handler.xsrf_validate() is None)
        
    
    

class TestHandlerRender(unittest.TestCase):
    """ Test the logic of `handler.render`.
    """
    
    def _make_one(self, *args, **kwargs):
        from thruflo.webapp.request import Handler
        return Handler(*args, **kwargs)
        
    
    def setUp(self):
        self.request = Mock()
        self.response = Mock()
        self.settings = {}
        self.template_renderer_adapter = Mock()
        self.static_url_generator_adapter = Mock()
        self.authentication_manager_adapter = Mock()
        self.secure_cookie_wrapper_adapter = Mock()
        self.method_selector_adapter = Mock()
        self.handler = self._make_one(
            self.request,
            self.response,
            self.settings,
            template_renderer_adapter=self.template_renderer_adapter,
            static_url_generator_adapter=self.static_url_generator_adapter,
            authentication_manager_adapter=self.authentication_manager_adapter,
            secure_cookie_wrapper_adapter=self.secure_cookie_wrapper_adapter,
            method_selector_adapter=self.method_selector_adapter
        )
        self.handler._xsrf_token = '...'
        
    
    def test_tmpl_name_passed_to_renderer(self):
        """ `tmpl_name` is passed to `self.template_renderer`.
        """
        
        self.handler.render('foo.tmpl')
        self.assertTrue(
            self.handler.template_renderer.render.call_args[0][0] \
            == 'foo.tmpl'
        )
        
    
    def test_params_passed_to_renderer(self):
        """ `params` are passed to `self.template_renderer` as exploded
          `**kwargs`.
        """
        
        params = dict(
            request=self.handler.request,
            current_user=self.handler.auth.current_user,
            get_static_url=self.handler.static.get_url,
            xsrf_input=self.handler.xsrf_input
        )
        self.handler.render('foo.tmpl')
        self.assertTrue(
            self.handler.template_renderer.render.call_args[1] == params
        )
        
    
    def test_kwargs_passed_to_renderer(self):
        """ `kwargs` are passed to `self.template_renderer` as exploded
          `**kwargs`.
        """
        
        self.handler.render('foo.tmpl', foo='bar')
        kwargs = self.handler.template_renderer.render.call_args[1]
        self.assertTrue(kwargs['foo'] == 'bar')
        
    
    def test_kwargs_overwrite_default_params(self):
        """ `kwargs` are passed to `self.template_renderer` as exploded
          `**kwargs`.
        """
        
        self.handler.render('foo.tmpl', request='bar')
        kwargs = self.handler.template_renderer.render.call_args[1]
        self.assertTrue(kwargs['request'] == 'bar')
        
    
    

class TestHandlerRedirect(unittest.TestCase):
    """ Test the logic of `handler.redirect`.
    """
    
    def _make_one(self):
        from thruflo.webapp.request import Handler
        return Handler(
            Mock(), Mock(), {},
            template_renderer_adapter=Mock(),
            static_url_generator_adapter=Mock(),
            authentication_manager_adapter=Mock(),
            secure_cookie_wrapper_adapter=Mock(),
            method_selector_adapter=Mock()
        )
        
    
    def setUp(self):
        from thruflo.webapp.request import webob_exceptions
        self.__status_map = webob_exceptions.status_map
        self.Moved301 = Mock()
        self.Found302 = Mock()
        webob_exceptions.status_map = {
            '301': self.Moved301,
            '302': self.Found302
        }
        self.handler = self._make_one()
        self.handler.request.get_response = Mock()
        self.handler.request.get_response.return_value = 'response'
    
    def tearDown(self):
        from thruflo.webapp.request import webob_exceptions
        webob_exceptions.status_map = self.__status_map
        
    
    def test_status_defaults_to_302(self):
        """ Uses `webob.exc.status_map['302'] by default.
        """
        
        self.handler.redirect('/foo')
        self.assertRaises(
            AssertionError,
            self.Moved301.assert_called_with,
            location='/foo'
        )
        self.Found302.assert_called_with(location='/foo')
        
    
    def test_status_301_if_permanent_is_true(self):
        """ Unless `permanent is True`.
        """
        
        self.handler.redirect('/foo', permanent=True)
        self.assertRaises(
            AssertionError,
            self.Found302.assert_called_with,
            location='/foo'
        )
        self.Moved301.assert_called_with(location='/foo')
        
    
    def test_status_301_if_permanent_is_literally_true(self):
        """ Note that's `permanent is True` not `permanent == True`.
        """
        
        self.handler.redirect('/foo', permanent=1)
        self.assertRaises(
            AssertionError,
            self.Moved301.assert_called_with,
            location='/foo'
        )
        
    
    def test_excclass_called_with_location_in_exploded_kwargs(self):
        """ ExceptionClass is called with exploded `**kwargs`, with 
          kwargs['location']` set to `location`.
        """
        
        self.handler.redirect('/foo', baz='blah')
        self.Found302.assert_called_with(baz='blah', location='/foo')
        
    
    def test_request_get_response_called_with_exc(self):
        """ Returns `request.get_response(exc)`.
        """
        
        self.Found302.return_value = 'exc'
        response = self.handler.redirect('/foo')
        self.handler.request.get_response.assert_called_with('exc')
        self.assertTrue(response == 'response')
        
    
    


class TestHandlerError(unittest.TestCase):
    """ Test the logic of `handler.error`.
    """
    
    def _make_one(self):
        from thruflo.webapp.request import Handler
        return Handler(
            Mock(), Mock(), {},
            template_renderer_adapter=Mock(),
            static_url_generator_adapter=Mock(),
            authentication_manager_adapter=Mock(),
            secure_cookie_wrapper_adapter=Mock(),
            method_selector_adapter=Mock()
        )
        
    
    def setUp(self):
        from thruflo.webapp.request import webob_exceptions
        self.__status_map = webob_exceptions.status_map
        self.ClientError = Mock()
        self.ServerError = Mock()
        webob_exceptions.status_map = {
            '400': self.ClientError,
            '500': self.ServerError
        }
        self.handler = self._make_one()
        self.handler.request.get_response = Mock()
        self.handler.request.get_response.return_value = 'response'
    
    def tearDown(self):
        from thruflo.webapp.request import webob_exceptions
        webob_exceptions.status_map = self.__status_map
        
    
    def test_exception_not_none(self):
        """ If `exception` is not `None`, returns 
          `request.get_response(exception)`.
        """
        
        response = self.handler.error(exception='not none')
        self.handler.request.get_response.assert_called_with('not none')
        self.assertTrue(response == 'response')
        
    
    def test_exception_none(self):
        """ If `exception` is `None`, which is the default, uses status
          to get ExceptionClass from `webob_exceptions.status_map`.
        """
        
        self.handler.error(status='500')
        self.assertRaises(
            AssertionError,
            self.ClientError.assert_called_with
        )
        self.ServerError.assert_called_with()
        self.handler.error(status='400')
        self.ClientError.assert_called_with()
        
    
    def test_status_can_be_int(self):
        """ `500` becomes `'500'`.
        """
        
        self.handler.error(status=500)
        self.ServerError.assert_called_with()
        
    
    def test_status_defaults_to_500(self):
        """ `status` defaults to `'500'`.
        """
        
        self.handler.error()
        self.ServerError.assert_called_with()
        
    
    def test_excclass_called_with_exploded_kwargs(self):
        """ ExceptionClass is called with exploded `**kwargs`.
        """
        
        self.handler.error(foo='bar', baz='blah')
        self.ServerError.assert_called_with(foo='bar', baz='blah')
        
    
    def test_request_get_response_called_with_exc(self):
        """ Returns `request.get_response(exc)`.
        """
        
        self.ServerError.return_value = 'exc'
        response = self.handler.error()
        self.handler.request.get_response.assert_called_with('exc')
        self.assertTrue(response == 'response')
        
    
    

