from rest_framework.views import exception_handler
from rest_framework.response import Response


def check_if_error_in_instance(exception_data):
    if isinstance(exception_data, list):
        for i in exception_data:
            if not isinstance(i, dict):
                return False
        return True
    else:
        return False


def exception_return_only_id(exc, context, instance):
    text = "{}s".format(instance)
    text_id = "{}_id".format(instance)

    response = exception_handler(exc, context)
    exception_data = response.data.get("data")
    if not check_if_error_in_instance(exception_data):
        return response

    request_data = context['request'].data["data"]
    response_data = {"validation_error": {text: []}}
    for index in range(len(exception_data)):
        if exception_data[index] != {}:
            response_data['validation_error'][text].append(
                {"id": request_data[index][text_id]})

    response_data.update({"errors": response.data})

    return Response(response_data, status=400)


def exception_couriers(exc, context):
    return exception_return_only_id(exc, context, "courier")


def exception_orders(exc, context):
    return exception_return_only_id(exc, context, "order")
