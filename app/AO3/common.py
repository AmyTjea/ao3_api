from . import utils
from .works import Work


def __setifnotnone(obj, attr, value):
    if value is not None:
        setattr(obj, attr, value)

def get_work_or_series_from_banner(banner):
    from .series import Series

    a = banner.h4.find_all("a")[0]

    if "/series" in a['href']:
        seriesid = a['href'].split("/")[-1]
        return Series(seriesid)

    return get_work_from_banner(banner)


def get_work_from_banner(work):    
    try:
        for a in work.h4.find_all("a"):
            workid = utils.workid_from_url(a['href'])
    except AttributeError:
        raise AttributeError
             
    new = Work(workid, load=True)
    return new

def url_join(base, *args):
    result = base
    for arg in args:
        if len(result) > 0 and not result[-1] == "/":
            result += "/"
        if len(arg) > 0 and arg[0] != "/":
            result += arg
        else:
            result += arg[1:]
    return result