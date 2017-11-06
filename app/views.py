from django.shortcuts import render
from django.http import HttpResponse

import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json



# Create your views here.

def index(req) :
    req = str(req)
    url = req.split("?")[1]
    url = url.split("=")[1]
    url = url[:-2]
    print(url)
    value = hand(url)
    return HttpResponse(value)



def hand(url) :

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = 'b7885b5fe5024d6993a9934d3ab0aa10'

    # Replace or verify the region.
    #ubscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

    requestHeaders = {
        # Request headers.
        # Another valid content type is "application/octet-stream".
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # The URL of a JPEG image containing handwritten text.

    # For printed text, set "handwriting" to false.
    params = {'handwriting' : 'true'}
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace 
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial s

    body = {'url' : url}


    try:
        # This operation requrires two REST API calls. One to submit the image for processing,
        # the other to retrieve the text found in the image. 
        #
        # This executes the first REST API call and gets the response.
        response = requests.request('POST', uri_base + '/vision/v1.0/RecognizeText', json=body, data=None, headers=requestHeaders, params=params)

        # Success is indicated by a status of 202.
        if response.status_code != 202:
            # if the first REST API call was not successful, display JSON data and exit.
            parsed = json.loads(response.text)
            print ("Error:")
            print (json.dumps(parsed, sort_keys=True, indent=2))
            exit()

        # The 'Operation-Location' in the response contains the URI to retrieve the recognized text.
        operationLocation = response.headers['Operation-Location']

        # Note: The response may not be immediately available. Handwriting recognition is an
        # async operation that can take a variable amount of time depending on the length
        # of the text you want to recognize. You may need to wait or retry this GET operation.

        print('\nHandwritten text submitted. Waiting 10 seconds to retrieve the recognized text.\n')
        time.sleep(10)

        # Execute the second REST API call and get the response.
        response = requests.request('GET', operationLocation, json=None, data=None, headers=requestHeaders, params=None)

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(response.text)
        datav = parsed['recognitionResult']['lines']
        val = ''
        for dat in datav:
            print (dat)
            val = val + dat['text'] + ''
        return val
    except Exception as e:
        print('Error:')
        print(e)
    
####################################