class ApiConfig:
    api_key = '6CSAoCCL7E2sgmPaSTTNGo2Y1eB0Dg'
    api_base = 'https://api.tej.com.tw'
    api_version = "1.0.0"
    page_limit = 100
    internal_detected = False
    ignoretz = False
    
    @staticmethod
    def info():
        from .connection import Connection
        import datetime
        path="apiKeyInfo/%s" % ApiConfig.api_key
        r = Connection.request('get', path).json()
        r['startDate']=datetime.datetime.strptime(r['startDate'],'%Y-%m-%d').date()
        if(r['endDate'] != None):
            r['endDate']=datetime.datetime.strptime(r['endDate'],'%Y-%m-%d').date()
        return r