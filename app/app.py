import sys
import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    Handles requests that are passed through an Amazon API Gateway REST API.
    GET, POST, and PUT requests all result in success codes that echo back input
    parameters in a message. DELETE requests result in a 405 response.

    Several kinds of REST API parameters are demonstrated:
    * Query string: 'name' can be sent in the query string,
      for example: demoapi?name=Martha
    * Custom header: 'day' can be sent as a custom header, for example: 'day: Thursday'
    * Body: 'adjective' can be sent in the request body, encoded as JSON,
      for example: {"adjective": "fantastic"}

    :param event: The event dict sent by Amazon API Gateway that contains all of the
                  request data.
    :param context: The context in which the function is called.
    :return: A response that is sent to Amazon API Gateway, to be wrapped into
             an HTTP response. The 'statusCode' field is the HTTP status code
             and the 'body' field is the body of the response.
    """
    logger.info(f"Request: {event}")
    response_code = 200
    # rds settings

    start_endpoint = "https://wnk07eo5oc.execute-api.eu-central-1.amazonaws.com/dev/v1/beekeepers"

    try:
        logger.info(f"asking {start_endpoint}")
        all_beekepers = requests.get(start_endpoint)
        logger.info("asked")
        # TODO: check if ok
        beekepers_dict = all_beekepers.json()
        logger.info(f"got all beekeepers! they are {len(beekepers_dict)}")
    except Exception as e: # TODO: check specific exceptions
        logger.error("ERROR: Unexpected error")
        logger.error(e)
        sys.exit()

    http_method = event.get('httpMethod')
    employees = event.get('employees')

    if http_method == 'GET':
        logger.info("inside get")
    else:
        logger.info(f"Sorry {http_method} isn't allowed.")
        response_code = 405

    response = {
        'statusCode': response_code,
        'body': json.dumps(all_beekepers)
    }

    logger.info(f"Response: {response}")

    return response
