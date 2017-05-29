import os
from collections import OrderedDict

from django.template.response import TemplateResponse
from django.views.generic import DetailView, View
from rules.contrib.views import permission_required
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, \
    route as wagtail_route
from wagtail.wagtailcore.models import Page

from bricks.utils import snake_case


class PageDetailView(DetailView):
    """
    A generic view implementation for wagtail's serve method.
    """
    page = None

    def get_object(self):
        return self.page

    def get_template_names(self):
        return self.page.get_template()

    def get_context_data(self, **kwargs):
        context = self.page.get_context(
            self.request, *self.args, **self.kwargs)
        context.update(kwargs)
        return context


def wrap_view_function_route(view, model, url, perms=None):
    perms = [perms] if isinstance(perms, str) else perms or ()

    @wagtail_route(url)
    def method(self, request, *args, **kwargs):
        view_func = lambda request: view(request, self, *args, **kwargs)
        for perm in perms:
            view_func = permission_required(perm)(view_func)
        return view_func(request)

    return method


def wrap_view_class_route(view, model, url, perms=None):
    perms = [perms] if isinstance(perms, str) else perms or ()

    @wagtail_route(url)
    def method(self, request, *args, **kwargs):
        view_func = view.as_view(page=self)
        for perm in perms:
            view_func = permission_required(perm)(view_func)
        return view_func(request, *args, **kwargs)

    return method


class RoutableViewsPage(RoutablePageMixin, Page):
    """
    This rendition of RoutableViewsPage makes it possible to define the views of all
    routes separately from the model.

    This architecture decouples two concerns that Wagtails puts into the same
    class:

    1) rendering a model through its views
    2) defining a model storage and business logic.

    Now we can separate both:

    .. code-block:: python

        # models.py
        from wagtail.wagtailcore.models import Page

        class BlogPage(Page):
            ...

    And a separate views.py file

    .. code-block:: python

        # views.py
        from .models import MyPage

        @BlogPage.register_route()
        def view_blog_page(request):
            response = do_some_logic()
            return response

        @BlogPage.register_route(r'comments/')
        def view_blog_page_comments(request):
            response = do_another_logic()
            return response

    """

    class Meta:
        abstract = True

    @classmethod
    def __load_views(cls):
        """
        Load the views module for the given app.
        """

        if cls.__dict__.get('_skip_load_views', False):
            return

        # Compute the views module path
        if hasattr(cls, 'views_module_path'):
            path = cls.views_path
            if path.startswith('.'):
                path = cls._meta.app_config.name + path
        else:
            mod_name = cls._meta.app_config.name
            path = mod_name + '.views'

        # Load views from all superclasses
        for superclass in cls.mro()[1:]:
            if issubclass(superclass, RoutableViewsPage):
                if superclass._meta.app_config:
                    superclass.__load_views()

        __import__(path)
        cls._skip_load_views = True

    @classmethod
    def __external_routes(cls):
        try:
            return cls.__dict__['_routablepage_external_routes']
        except KeyError:
            routes = getattr(cls, '_routablepage_external_routes', [])
            cls._routablepage_external_routes = list(routes)
            return cls._routablepage_external_routes

    @classmethod
    def get_subpage_urls(cls):
        cls.__load_views()

        routes = []
        for attr in dir(cls):
            val = getattr(cls, attr, None)
            if hasattr(val, '_routablepage_routes'):
                routes.extend(val._routablepage_routes)
        routes.extend(cls.__external_routes())
        routes.sort(key=lambda route: route[1])
        routes = OrderedDict((route.regex, route) for route, idx in routes)
        return tuple(routes.values())

    @classmethod
    def register_route(cls, url=r'^$', name=None, perms=None,
                       login_required=False):
        """
        A decorator that register a function to be a route for the given model
        and url pattern.

        .. code-block:: python

            # views.py

            from .models import BlogPost

            @BlogPost.register_route(r'^comments/$')
            def view_comments(request, page):
                return render(request, 'blog/post.html', ...)

        Args:
            url:
                A regex matching the desired url.
            name:
                The name of the route. Be careful to pick unique and meaningful
                names since we are in a global namespace.
            perms:
                An optional list of permissions required to access the given
                route.
        """

        def decorator(view):
            if isinstance(view, type) and issubclass(view, View):
                method = wrap_view_class_route(view, cls, url, perms=perms)
            else:
                method = wrap_view_function_route(view, cls, url, perms=perms)
            method.__name__ = view.__name__
            urlpattern, idx = method._routablepage_routes[-1]
            urlpattern.name = name or view.__name__
            cls.__external_routes().append((urlpattern, idx))
            if url in [None, '', '^$', '/']:
                cls._view_for_root_url = method
            return view

        return decorator

    @classmethod
    def __get_context_names(cls):
        varname = '_context_names_'
        if varname not in cls.__dict__:
            names = []
            for subclass in cls.mro():
                if issubclass(subclass, Page):
                    name = snake_case(subclass.__name__)
                    names.append(name)
            setattr(cls, varname, names)
        return cls.__dict__[varname]

    def get_context(self, request, *args, **kwargs):
        names = self.__get_context_names()
        ctx = super().get_context(request, *args, **kwargs)
        for name in names:
            ctx.setdefault(name, self)
        return ctx

    def get_template(self, request, *args,
                     suffix=None, basename=None,
                     **kwargs):
        template = super(RoutableViewsPage, self).get_template(request, *args,
                                                               **kwargs)
        templates = [template] if isinstance(template, str) else list(template)
        if templates[-1].endswith('.html'):
            templates.append(templates[-1][:-5] + '.jinja2')

        # Replace basename
        if basename:
            splitext = os.path.splitext
            dirname = os.path.dirname
            join = os.path.join
            templates = (splitext(x) for x in templates)
            templates = [join(dirname(base), basename + ext)
                         for (base, ext) in templates]

        # Add suffix before extension
        if suffix:
            splitext = os.path.splitext
            templates = (splitext(x) for x in templates)
            templates = [base + suffix + ext for (base, ext) in templates]

        return templates

    def serve(self, request, *args, **kwargs):
        if not args and not kwargs and hasattr(self, '_view_for_root_url'):
            return self._view_for_root_url(request)
        return super().serve(request, *args, **kwargs)
