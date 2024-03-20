class Title(object):
    """ "
    Update title and favicon of each page
    ⚠️ IMPORTANT: Must call page_config() as first function in script
    """

    def __init__(self):
        self.img = "images/JobsonLogoNavbar.png"

    def page_config(self, title):
        self.title = title
        # st.set_page_config(page_title=self.title, page_icon=self.img)
