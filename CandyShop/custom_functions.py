from CandyShop import serializers


def convert_courier_type_to_weight(courier_type):
    if courier_type == 'foot':
        return 10
    if courier_type == 'bike':
        return 15
    if courier_type == 'car':
        return 50


def check_time_intervals(working_hours, delivery_hours):
    for work in working_hours:
        for delivery in delivery_hours:
            work_time = serializers.TimeInterval(work)
            delivery_time = serializers.TimeInterval(delivery)
            if not (delivery_time.end < work_time.start or work_time.end < delivery_time.start):
                return True
    return False