# API Work

## setting up environment

set up docker container for running fastapi server

* one for dev
  -one for staging
* one for prod

## Modules to modify/ extend

OTHER LAST DO THIS

* \[] factor out the request method out of chapters, series, session and user modules, put into utils/ into a base class?
* \[] find the



improve way pages are requested from, make shared util o



Works THEN DO THIS AND

* \[v] allow getting bookmarkers
* add url to metadata for works
* add series for the 
* \[] Update method to find the number of pages (in func bookmarkers + in the users file under func \_bookmarks\_pages. potentially write a util function which can find this value w/o iteration (just get the 2nd last li object))
* \[] allow seeing who has publicly kudosed a fic



Users DO THIS FIRST, THEN EXPOSE TO API

* \[v] update bookmarks? (can now handle series and works)
* \[v] update how bookmarks + series gotten from banner (need to figure out handling error Pages (getting issues as getting the 503 ao3 is responding slowly
* \[] remove session and other related functions
* \[v] add ability to handle profile data + bio + other stuff

Chapters

Comments

collections

Extra

Search



Series

* add bookmarks (bookmarkers)

Bookmark (new?)

* create bm object
* infomation

  * work object
  * bookmarker
  * date bookmarked
  * bookmark notes
  * bookmark tags
  * bookmark collections

Session

* likely remove (want mainly read only /get only functionality)



## Modules to Fast API-ify

Users
Chapters

Comments

collections

Extra

Search



Series

# other work

Look into developing a schema for consistency

