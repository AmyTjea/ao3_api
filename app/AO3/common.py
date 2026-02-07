from . import utils

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
    #* These imports need to be here to prevent circular imports
    #* (series.py would require common.py and vice-versa)
    from .works import Work

    try:
        a = work.h4.find_all("a")[0] # first link wll be the work link
        workid = utils.workid_from_url(a['href'])
    except AttributeError:
        raise AttributeError

    new = Work(workid, load=True,load_chapters=False)
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