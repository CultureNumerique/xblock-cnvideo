import pkg_resources
import requests

from urlparse import urlparse

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment 

class CNVideoBlock(XBlock):
    """
    An XBlock to deal with videos imported in Culture Numerique online courses
    Aims at supporting vimeo<http://vimeo.com> and CanalU <https://www.canal-u.tv/> videos
    """
    
    href = String(help="URL of the video link at the provider", default=None, scope=Scope.content)
    maxwidth = Integer(help="Max width of the video", default="480", scope=Scope.content)
    maxheight = Integer(help="Max height of the video", default="270", scope=Scope.content)
    watched_count = Integer(help="Number of times the video has been watched", default=0, scope=Scope.user_state)
    
    def student_view(self, context):
        """
        Generate the html code to display the XBlock to a student
        `context` is a dictionary used to configure the display (unused).

        Returns a `Fragment` object specifying the HTML, CSS, and JavaScript
        to display.
        """
        provider, embed_code = self.get_embed_code_for_url(self.href)
        
        # Retrieve HTML code for video iframe 
        html_code = pkg_resources.resource_string(__name__, "cnvideo/static/html/cnvideo.html")
        frag = Fragment(unicode(html_code).format(self=self, embed_code=embed_code))
        
        # Load CSS
        css_str = pkg_resources.resource_string(__name__, "cnvideo/static/css/cnvideo.css")
        frag.add_css(unicode(css_str))
        
        # Load vimeo JS API and custom js for watching views
        if provider == "vimeo.com":
            frag.add_javascript_url("//f.vimeocdn.com/js/froogaloop2.min.js")
            js_str = pkg_resources.resource_string(__name__, "cnvideo/static/js/cnvideo.js")
            frag.add_javascript(unicode(js_str))
            frag.initialize_js("CNVideoBlock")
        
        return frag
        
    def studio_view(self, context):
        """
        Allows to edit cnvideo components
        """
        html_code = pkg_resources.resource_string(__name__, "cnvideo/static/html/cnvideo_edit.html")
        href = self.href or ''
        frag = Fragment(unicode(html_code).format(href=href, maxwidth=self.maxwidth, maxheight=self.maxheight))
        
        js_str = pkg_resources.resource_string(__name__, "cnvideo/static/js/cnvideo_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('cnVideoEditBlock')
        
        return frag
        
        
    
    def get_embed_code_for_url(self, url):
        """
        parses a given url and retrieve embed code
        """
        hostname = url and urlparse(url).hostname
        # check provider is supported
        if hostname == "vimeo.com":
            oembed_url = 'https://vimeo.com/api/oembed.json'
            
        elif hostname == "canal-u.tv":
            # build embed url from template
            # ex : https://www.canal-u.tv/video/universite_de_tous_les_savoirs/pourquoi_il_fait_nuit.1207 == hostname/video/[channel]/[videoname] 
            return hostname, '<p>Support for Canal-u.tv coming soon...({0})</p>'.format(hostname)
        else:
            return hostname, '<p>Unsupported video provider ({0})</p>'.format(hostname)
        
        # For vimeo videos, use OEmbed API
        params = {
            'url': url,
            'format':'json',
            'maxwidth':self.maxwidth,
            'maxheight':self.maxheight,
            'api':True 
        }
        
        try:
            r = requests.get(oembed_url, params=params)
            r.raise_for_status()
        except Exception as e:
            return hostname, '<p>Error getting video from provider ({error})</p>'.format(error=e)
        
        res = r.json()
        return hostname, res['html']
    
    @XBlock.json_handler
    def mark_as_watched(self, data, suffix=''):
        """
        (Vimeo only) Method called each time the video has been watched using Froogaloop API
        see cnvideo/static/js/cnvideo.js
        """
        if data.get('watched'):
            self.watched_count+=1
            
        return {'watched_count': self.watched_count}
        
    @XBlock.json_handler
    def studio_save(self, data, suffix=''):
        """
        Handles save action in the EdxStudio edit form
        """
        self.href = data.get('href')
        self.maxwidth = data.get('maxwidth')
        self.maxheight = data.get('maxheight')
        
        return {'result': 'success'}
    
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CN video",
            """
            <vertical_demo>
                <cnvideo href="https://vimeo.com/122104210" maxwidth="800" />
            </vertical_demo>
            """)
        ]
    
        
        
        