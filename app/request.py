import urllib.request,json
from .models import Quote

#qoutes base url
base_url=None

def configure_request(app):
    global base_url
    base_url=app.config['QUOTES_BASE_URL']

def get_quotes():
    '''
    Function that fetches the json response from the url
    '''  

    get_quotes_url=base_url

    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes_data=url.read()
        get_quotes_response=json.loads(get_quotes_data)

        quote_obj=None
        if get_quotes_response:
            id=get_quotes_response.get('id')
            author=get_quotes_response.get('author')
            qoute=get_quotes_response.get('quote')

            quote_obj=Quote(id,author,qoute)
    
    return quote_obj   
