from rest_framework.views import exception_handler
from rest_framework.response import Response


def exception_couriers(exc, context):
    response = exception_handler(exc, context)
    exception_data = response.data.get("data")
    if isinstance(exception_data, list):
        for i in exception_data:
            if not isinstance(i, dict):
                return response
    else:
        return response

    request_data = context['request'].data["data"]
    response_data = {"validation_error": {"couriers": []}}
    for courier_index in range(len(exception_data)):
        response_data['validation_error']['couriers'].append({"id": request_data[courier_index]["courier_id"]})

    return Response(response_data, status=400)
