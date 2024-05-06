from urllib import request
from xml.dom.minidom import parseString

class RulesClient:

    def __init__(self, rest_url):
        self.rest_url = rest_url
        self.token = 'Xe3SoIt7Akz2bYV52EqHVdRHP0ARzrrN6CleOrHtPn4Dd8RdH%2FN0BeSkokzqnRmta6qgxEBEmh3UwtRJfv%2FCos3yWXIC58dFvr1QmlFXDKewMIL9Caj8LHNsaQZK5pE9%2FkGGKppRRexbtzwEhv0Itd21mH4CICZO7G6XGchKXLURS5raVFp5ubeInzkRuCIUSK2PdS80HE9Ge8gfYoIftBzTtl6hgOQFaaZYyQAFFAMWyNFSpyC29iyTgHpaobqv' 
        self.default_params = {'loginToken':self.token}

    def build_url(self, path, params={}):
        path = f"{self.rest_url}/{path}?loginToken={self.token}"
        for k,v in params.items():
            path = f"{path}&{k}={v}"
        #print(path)
        return path

    def get_url(self, url):
         req = request.Request(url)
         response = request.urlopen(req)
         return response.read()

    def post_url(self, url, data=None, xml=True):
         if xml:
            headers = {
               'Content-Type': 'application/xml' # Set content type to XML
            }
         print(headers)
         req = request.Request(url, data, headers)
         response = request.urlopen(req)
         return response.read()

    def read_xml_from_file(self, file='xml/calc.xml'):
         buf = open(file).read()
         return buf

    def get_jurisdictions(self):
        path = "jurisdictions/my"
        url = self.build_url(path)
        return self.get_url(url)

    def get_triggers(self, system_id):
        path =  "triggers"
        params = { "jurisdictionSystemID": system_id }
        url = self.build_url(path, params)
        return self.get_url(url)

    def compute_dates(self, jurisdiction_id, trigger_id, date, system_id=None):
        path = "compute/dates"
        url = self.build_url(path)
        data = self.read_xml_from_file(file='xml/calc.xml')
        data = data.replace("{jurisdiction_id}",str(jurisdiction_id))
        data = data.replace("{trigger_id}",str(trigger_id))
        data = data.replace("{date}",date)
        data = data.encode('utf-8')
        return self.post_url(url,data)

    def pretty_print(self, data):
        buf = parseString(data)
        print(buf.toprettyxml())

if __name__ == "__main__":
    url = "https://test.crcrules.com/CalendarRulesService.svc/rest"

    # get jurisdictions
    c = RulesClient(url)
    buf = c.get_jurisdictions()
    #c.pretty_print(buf)

    # get triggers
    buf = c.get_triggers(-10279)
    #c.pretty_print(buf)

    # calculate dates
    buf = c.compute_dates(-10279,-4322,"2024-05-31T11:20:00")
    c.pretty_print(buf)
