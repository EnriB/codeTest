import sys
import json
import logging
import pymysql
import rds_config

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

    rds_host = "test-db.c4mjga2zcbkb.us-east-1.rds.amazonaws.com"
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name

    try:
        mydb = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        mycursor = mydb.cursor()
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    http_method = event.get('httpMethod')
    employees = event.get('employees')
    # headers = event.get('headers')
    # body = event.get('body')

    if http_method == 'GET':
        logger.info(f"Nice GET with employees {employees}")
        ids = [x['id'] for x in employees]

        query = f"SELECT * FROM Employee WHERE EmpId IN (%s,)"
        mycursor.execute(query, ids)
        result = mycursor.fetchall()
        json_ready = [dict((mycursor.description[i][0], value)
                      for i, value in enumerate(row)) for row in result]
    elif http_method == 'POST':
        logger.info(f"Nice POST with {employees}")
        query = "INSERT INTO Employee (EmpID, Name) values (%s, %s)"
        val = [(x['id'], x['name']) for x in employees]
        mycursor.executemany(query, val)
        mydb.commit()
        json_ready = {'query': query}
        logger.info(f"{mycursor.rowcount} rows were inserted.")
    else:
        logger.info(f"Sorry {http_method} isn't allowed.")
        response_code = 405

    response = {
        'statusCode': response_code,
        'body': json.dumps(json_ready)
    }

    logger.info(f"Response: {response}")

    return response
