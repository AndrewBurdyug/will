import datetime
import requests
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
from will import settings

class TimePlugin(WillPlugin):


    @respond_to("what time is it in (?P<place>.*)")
    def what_time_is_it_in(self, message, place):
        print "responding to in"
        if not hasattr(settings, "WORLD_WEATHER_ONLINE_KEY"):
            self.say("I need a world weather online key to do that.\n You can get one at http://developer.worldweatheronline.com, and then set the key as WORLD_WEATHER_ONLINE_KEY", message=message)
        else:
            r = requests.get("http://api.worldweatheronline.com/free/v1/tz.ashx?q=%s&format=json&key=%s" % (place, settings.WORLD_WEATHER_ONLINE_KEY))
            resp = r.json()
            print resp
            place = resp["data"]["request"][0]["query"]
            current_time = self.parse_natural_time(resp["data"]["time_zone"][0]["localtime"])

            self.say("It's %s in %s." % (self.to_natural_day_and_time(current_time), place), message=message)

    @respond_to("what time is it(\?)?$", multiline=False)
    def what_time_is_it(self, message):
        now = datetime.datetime.now()
        self.say("It's %s." % self.to_natural_day_and_time(now), message=message)
