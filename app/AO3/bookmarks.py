from abc import ABC, abstractmethod

from .utils import workid_from_url, username_from_url

class BookmarkBase(ABC):
    def __init__(self,soup_bookmark):        
        self._load_details_from_bookmark(soup_bookmark)
        self._find_bookmark_details(soup_bookmark)

    @abstractmethod
    def _load_details_from_bookmark(self,banner):
        pass

    def _find_bookmark_details(self,bookmark):
        # # Bookmarker username
        # self.bookmarker_username = bookmark.find("h5", class_="byline heading").find("a")

        # Bookmark date
        bookmark_date_tag = bookmark.find("p", class_="datetime")
        self.bookmark_date = bookmark_date_tag.text.strip() if bookmark_date_tag else ""

        # Bookmarker's tags
        self.bookmarker_tags = [a.text.strip() for a in bookmark.select("ul.meta.tags a")]

        # Bookmarker's collections
        ## TODO: get urls for the collections class
        self.bookmarker_collections = [a.text.strip() for a in bookmark.select("ul.meta.commas:not(.tags) > li > a")]


        # Bookmarker's notes (check multiple possible classes)
        notes_tag = bookmark.find("blockquote", class_="userstuff notes")
        if not notes_tag:
            notes_tag = bookmark.find("blockquote", class_="userstuff summary")
        self.notes = notes_tag.text.strip() if notes_tag else ""

    


class UserBookmark(BookmarkBase):
    """ Bookmarks stored by users
    """
    def __init__(self,soup_bookmark):
        super().__init__(soup_bookmark)

    def _load_details_from_bookmark(self,banner):
        self.bookmark= self.get_work_or_series_from_banner(banner)


    def get_work_or_series_from_banner(self,banner):
        from .series import Series


        a = banner.h4.find_all("a")[0]

        if "/series" in a['href']:
            seriesid = a['href'].split("/")[-1]
            self.type = "series"
            return Series(seriesid)

        return self.get_work_from_banner(banner)


    def get_work_from_banner(self,work):    
        #* These imports need to be here to prevent circular imports
        #* (series.py would require common.py and vice-versa)
        from .works import Work

        self.type = "work"

        try:
            a = work.h4.find_all("a")[0] # first link wll be the work link
            workid = workid_from_url(a['href'])
        except AttributeError:
            raise AttributeError

        new = Work(workid, load=True,load_chapters=False)
        return new
    
    def __repr__(self):

        return f"<{self.__class__.__name__} {self.type}={self.bookmark}>"
    

    def __str__(self):

        return (

            f"Date bookmarked: {self.bookmark_date}\n"
            f"Bookmarker Tags: {self.bookmarker_tags or 'None'}\n"
            f"Bookmarker Collections: {self.bookmarker_collections or 'None'}\n"
            f"Bookmarker Notes: {self.notes or 'None'}"
            f"{self.bookmark}"
        )




class Bookmarker(BookmarkBase):
    """Bookmarks stored by works/series
    """
    def __init__(self,soup_bookmark):
        super().__init__(soup_bookmark)

    def _load_details_from_bookmark(self,banner):
        from .users import User

        #might need to import here

        h5 = banner.find("h5")
        url = h5.find("a")["href"]

        username = username_from_url(url)
        # Don't convert 
        self.bookmarker= User(username,load=False) # type user, if being used by user class dont need as user class holds
        # self.bookmarker= username # type user, if being used by user class dont need as user class holds


    
    def __repr__(self):

        return f"<{self.__class__.__name__} Bookmarker ={self.bookmarker}>"
    

    def __str__(self):

        return (
            f"{self.bookmarker}"
            f"Date bookmarked: {self.bookmark_date}\n"
            f"Bookmarker Tags: {self.bookmarker_tags or 'None'}\n"
            f"Bookmarker Collections: {self.bookmarker_collections or 'None'}\n"
            f"Bookmarker Notes: {self.notes or 'None'}"
        )


# TODO: Make util to parse form banner