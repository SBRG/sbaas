from version import __version__
import json

# TODO remove all os.path.join when using urls

class urls():

    def __init__(self):

        self._visualization_css = json.load(open('visualization\\resources\\urls_visualization_css.json'));

        self._visualization_js = json.load(open('visualization\\resources\\urls_visualization_js.json'));

        self._visualization_data_dir = json.load(open('visualization\\resources\\urls_visualization_data_dir.json'));

        self._resources = json.load(open('visualization\\resources\\urls_resources.json'));
    
        self._dependencies = json.load(open('visualization\\resources\\urls_dependencies.json'));
    
        self._dependencies_cdn = json.load(open('visualization\\resources\\urls_dependencies_cdn.json'));

        self._links = json.load(open('visualization\\resources\\urls_links.json'));

        # external dependencies
        self.names = self._visualization_css.keys() + self._visualization_js.keys() + self._visualization_data_dir.keys() + self._resources.keys() + self._dependencies.keys() + self._links.keys()

    def get_url(self, name, source='web', local_host=None, protocol=None):
        """Get a url.

        Arguments
        ---------

        name: The name of the URL. Options are available in urls.names.

        source: Either 'web' or 'local'. Cannot be 'local' for external links.

        protocol: The protocol can be 'http', 'https', or None which indicates a
        'protocol relative URL', as in //zakandrewking.github.io/escher. Ignored if
        source is local.

        local_host: A host url, including the protocol. e.g. http://localhost:7778.

        """
        if source not in ['web', 'local']:
            raise Exception('Bad source: %s' % source)
    
        if protocol not in [None, 'http', 'https']:
            raise Exception('Bad protocol: %s' % protocol)

        if protocol is None:
            protocol = ''
        else:
            protocol = protocol + ':'

        def apply_local_host(url):
            return '/'.join([local_host.rstrip('/'), url])
        
        # visualization_css
        if name in self._visualization_css:
            if source=='local':
                if local_host is not None:
                    return apply_local_host(self._visualization_css[name])
                return self._visualization_css[name]
            return protocol + self._links['github'] + '/visualization/' + self._visualization_css[name]
        # visualization_js
        elif name in self._visualization_js:
            if source=='local':
                if local_host is not None:
                    return apply_local_host(self._visualization_js[name])
                return self._visualization_js[name]
            return protocol + self._links['github'] + '/visualization/' + self._visualization_js[name]
        # visualization_data
        elif name in self._visualization_data_dir:
            if source=='local':
                if local_host is not None:
                    return apply_local_host(self._visualization_data_dir[name])
                return self._visualization_data_dir[name]
            return protocol + self._links['github'] + '/visualization/' + self._visualization_data_dir[name]
        # resources
        elif name in self._resources:
            if source=='local':
                if local_host is not None:
                    return apply_local_host(self._resources[name])
                return self._resources[name]
            return protocol + self._links['github'] + '/visualization/' + self._resources[name]
        # links
        elif name in self._links:
            if source=='local':
                raise Exception('Source cannot be "local" for external links')
            return protocol + self._links[name]
        # local dependencies
        elif name in self._dependencies and source=='local':
            if local_host is not None:
                return apply_local_host(self._dependencies[name])
            return self._dependencies[name]
        # cdn dependencies
        elif name in self._dependencies_cdn and source=='web':
            return protocol + self._dependencies_cdn[name]
        else:
            raise Exception('name not found')

    def data_name_to_url(self, dir, name, protocol='https'):
        """Convert short name to url.

        """
        parts = name.split(':')
        if len(parts) != 2:
            raise Exception('Bad model name')
        longname = name + '.js';
        return '/'.join([get_url(dir, source='web', protocol=protocol), longname])
