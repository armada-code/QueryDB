import azure.functions as func
import logging




from dbquery import createClient





app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="funct_http_trigger_db")
def funct_http_trigger_db(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    deviceId = req.params.get('deviceId')
    if not deviceId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            deviceId = req_body.get('deviceId')

    if deviceId:
        data = createClient(deviceId);
        return func.HttpResponse(f"Hello, {data}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
