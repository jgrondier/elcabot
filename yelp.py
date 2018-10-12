from yelpapi import YelpAPI

def search_yelp(business_type, location):
    yelp_api = YelpAPI('mycs0Rr2L8hy4QUL_cvA5Kyv2i7iCqgFR84V29ZW1TqIsWO7MQjunW8deES8-1g6hDuFfout3x-r1706Xi_qSjUutX3olWO-RlCqghBselLBu9J5v7x6YOEBXFzAW3Yx')
    search_results = yelp_api.search_query(term=business_type, location=str(location['latitude'])+","+str(location['longitude']))
    first_result = search_results['businesses'][0]
    venueLocation = (first_result['coordinates']['latitude'], first_result['coordinates']['longitude'])
    venueName = first_result['name']
    return {'location':venueLocation, 'name':venueName}
