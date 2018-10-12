from yelpapi import YelpAPI
#import pprint

def search_yelp(business_type, location, limit = 5):
    yelp_api = YelpAPI('YELP TOKEN')
    search_results = yelp_api.search_query(term=business_type, location=str(location['latitude'])+","+str(location['longitude']))
    results = search_results['businesses'][:limit]
    return [{'location':(result['coordinates']['latitude'], result['coordinates']['longitude']), 'name':result['name'], 'url': result['url'], 'display_address': ', '.join(result['location']['display_address'])} for result in results]  

    
#pprint.pprint(search_yelp("restaurant", {'latitude': 46.522951, 'longitude': 6.564554}, limit = 10))