import time
class ResultsProxy(object):

    def __init__(self, es, index=None, body=None):
        self.es = es
        self.index = index
        self.body = body

    def __len__(self):
        result = self.es.count(index=self.index,
                               body=self.body)
        return result['count']

    def __getitem__(self, item):
        assert isinstance(item, slice)

        results = self.es.search(
            index=self.index,
            body=self.body,
            from_=item.start,
            size=item.stop - item.start,
        )
        return results['hits']['hits']

    def __getitembydate__(self, item):
        results = self.es.search(
            index=self.index,
            body=self.body,
            size = 10000
        )
        tmp = results['hits']['hits']
        if(item["date1"] != ""):
            date1 = time.strptime(item["date1"], "%Y-%m-%d")
        else:
            date1 = time.strptime("1800-01-01", "%Y-%m-%d")
        if(item["date2"] != ""):
            date2 = time.strptime(item["date2"], "%Y-%m-%d")
        else:
            date2 = time.strptime("2100-12-31", "%Y-%m-%d")
        i=0
        res = []
        for it in tmp:
            xxx = it['_source']['upload_time'].split(",")
            time_upload = time.strptime(xxx[0], "%d/%m/%Y")
            if((time_upload > date2) or (time_upload < date1)):
                #it['_source']['description'] = "123"
                it['_source']['ishide'] = True
            else:
                it['_source']['ishide'] = False
                res.append(it)
                i+=1
            
        start = item["start"]
        end = item["end"]
        obj = {}
        obj["tmp"] = res[start:end]
        obj["count"] = i
        return obj 

