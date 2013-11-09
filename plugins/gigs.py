# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from util import hook, http, timesince

#
# Prints the date, venue, city and country of the given artist
#
#


api_url = "http://ws.audioscrobbler.com/2.0/?format=json"
maxgigs=5

@hook.command('gi', autohelp=False)
@hook.command(autohelp=False)
def gigs(inp, conn=None, bot=None,nick=None, chan=None):
    """gigs [band] -- Displays the band's gigs
     from lastfm db."""
    api_key = bot.config.get("api_keys", {}).get("lastfm")
    if not api_key:
        return "error: no api key set"

    r = http.get_json(api_url, method="artist.getEvents",
                             api_key=api_key, artist=inp,autocorrect=1,limit=maxgigs)

    if 'error' in r:
        return "Error: {}.".format(r["message"])

    llimit=str(r["events"]["@attr"]["total"] if r["events"]["@attr"]["total"] < maxgigs else maxgigs)

    if type(r) == dict and "event" in r["events"] and type(r["events"]["event"]) == list:
        conn.send("PRIVMSG {} :\x01ACTION will headbang at these {} gigs with {}:\x01".format(chan,llimit,nick))
        for event in r["events"]["event"]:
            headliner = event["artists"]["headliner"] if "headliner" in event["artists"] else "TBA"
            conn.send(u"PRIVMSG {} :{}:\t{} ({},{}), headliner: {}, artists: {}".format(chan,event["startDate"],event["venue"]["name"],event["venue"]["location"]["city"],event["venue"]["location"]["country"],headliner,", ".join(event["artists"]["artist"])))
    else:
        conn.send(u"PRIVMSG {} :{}, No gigs for {} :(".format(chan,nick,inp))