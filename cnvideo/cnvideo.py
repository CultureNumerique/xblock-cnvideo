from __future__ import division
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
    
    href = String(help="URL of the video link at the provider", default="https://vimeo.com/122104210", scope=Scope.content)
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
        html_code = pkg_resources.resource_string(__name__, "static/html/cnvideo.html")
        frag = Fragment(unicode(html_code).format(self=self, embed_code=embed_code))
        
        # Load CSS
        css_str = pkg_resources.resource_string(__name__, "static/css/cnvideo.css")
        frag.add_css(css_str)
        
        # Load vimeo JS API and custom js for watching views
        if provider == "vimeo.com":
            frag.add_javascript_url("//f.vimeocdn.com/js/froogaloop2.min.js")
            js_str = pkg_resources.resource_string(__name__, "static/js/cnvideo.js")
            frag.add_javascript(unicode(js_str))
            frag.initialize_js("cnVideoBlock")
        
        return frag
        
    def studio_view(self, context):
        """
        Allows to edit cnvideo components
        """
        html_code = pkg_resources.resource_string(__name__, "static/html/cnvideo_edit.html")
        href = self.href or ''
        frag = Fragment(unicode(html_code).format(href=href))
        
        js_str = pkg_resources.resource_string(__name__, "static/js/cnvideo_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('cnVideoEditBlock')
        
        return frag
        
        
    
    def get_embed_code_for_url(self, url):
        """
        parses a given url and retrieve embed code
        """
        hostname = url and urlparse(url).hostname
        # VIMEO case
        if hostname == "vimeo.com":
            # For vimeo videos, use OEmbed API
            params = { 'url': url, 'format':'json', 'api':True }
            try:
                r = requests.get('https://vimeo.com/api/oembed.json', params=params)
                r.raise_for_status()
            except Exception as e:
                return hostname, '<p>Error getting video from provider ({error})</p>'.format(error=e)
            res = r.json()
            return hostname, res['html']
            
        # CanalU.tv
        elif hostname == "www.canal-u.tv":
            # build embed url from template
            # ex : https://www.canal-u.tv/video/universite_de_tous_les_savoirs/pourquoi_il_fait_nuit.1207 == hostname/video/[channel]/[videoname] 
            embed_code = """<iframe src="{0}/embed.1/{1}?width=100%&amp;height=100%&amp" width="550" height="306" frameborder="0" allowfullscreen scrolling="no"></iframe>""".format(url.rsplit('/', 1)[0],url.split('/')[-1])
            return hostname, embed_code
        
        # not supported
        else:
            return hostname, '<p>Unsupported video provider ({0})</p>'.format(hostname)
        
        
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
        
        return {'result': 'success'}
    
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CN video",
            """
            <vertical_demo>
                <cnvideo href="http://www.canal-u.tv/video/universite_paris_diderot/13min_qui_suis_je_entre_genetique_et_epigenetique_jonathan_weitzman.12437" />
            </vertical_demo>
            """)
        ]
    