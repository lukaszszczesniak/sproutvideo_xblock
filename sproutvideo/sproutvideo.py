"""TO-DO: Write a description of what this XBlock is."""

from importlib.resources import files

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String


class SproutVideoXBlock(XBlock):
    """
    XBlock for embedding SproutVideo videos via iframe.
    """

    display_name = String(
        display_name="Display Name",
        default="SproutVideo Player",
        scope=Scope.settings,
        help="Name shown in the Studio interface"
    )

    icon_class = "video"  # lub inna ikona, np. "other"

    video_url = String(
        display_name="SproutVideo Embed URL",
        default="https://videos.sproutvideo.com/embed/0691dbbe1f19e1c78f/9ee82871e80eda13",
        scope=Scope.content,
        help="Embed URL from SproutVideo"
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        return files(__package__).joinpath(path).read_text(encoding="utf-8")

    def student_view(self, context=None):
        """
        The primary view of the SproutVideoXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/sproutvideo.html")
        rendered_html = html.format(video_url=self.video_url)
        frag = Fragment(rendered_html)
        frag.add_css(self.resource_string("static/css/sproutvideo.css"))
        frag.add_javascript(self.resource_string("static/js/src/sproutvideo.js"))
        frag.initialize_js('SproutVideoXBlock')
        return frag


    def studio_view(self, context=None):
        """
        View shown to course authors in Studio.
        """
        html = self.resource_string("static/html/sproutvideo_edit.html")
        rendered_html = html.format(video_url=self.video_url)
        frag = Fragment(rendered_html)
        frag.add_css(self.resource_string("static/css/sproutvideo.css"))
        frag.add_javascript(self.resource_string("static/js/src/sproutvideo_edit.js"))
        frag.initialize_js('SproutVideoEditXBlock')
        return frag


    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("SproutVideoXBlock",
             """<sproutvideo/>
             """),
            ("Multiple SproutVideoXBlock",
             """<vertical_demo>
                <sproutvideo/>
                <sproutvideo/>
                <sproutvideo/>
                </vertical_demo>
             """),
        ]

    @XBlock.json_handler
    def save_video_url(self, data, suffix=''):
        """
        Handler to save the video URL from Studio.
        """
        url = data.get('video_url', '').strip()
        if not url.startswith('https://videos.sproutvideo.com/embed/'):
            return {"result": "error", "message": "Invalid SproutVideo embed URL."}
        self.video_url = url
        return {"result": "success"}
