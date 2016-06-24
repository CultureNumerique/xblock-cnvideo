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
    
    
    def student_view(self, context):
        """
        Generate the html code to display the XBlock to a student
        `context` is a dictionary used to configure the display (unused).

        Returns a `Fragment` object specifying the HTML, CSS, and JavaScript
        to display.
        """
        provider, embed_code = self.get_embed_code_for_url(self.href)
        
        # Retrieve HTML code for video iframe 
        html_code = pkg_resources.resource_string(__name__, "static/html/cnvideo.html")
        frag = Fragment(unicode(html_code).format(self=self, embed_code=embed_code))
        
        return frag
        
        
    def get_embed_code_for_url(self, url):
        """
        parses a given url and retrieve embed code
        """
        hostname = (url and urlparse(url).hostname)
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
        
        
        
        
        