from CandyShop import serializers


def convert_courier_type_to_weight(courier_type):
    if courier_type == 'foot':
        return 10
    if courier_type == 'bike':
        return 15
    if courier_type == 'car':
        return 50


def convert_courier_type_to_coef(courier_type):
    if courier_type == 'foot':
        return 2
    if courier_type == 'bike':
        return 5
    if courier_type == 'car':
        return 9


def convert_datetime_to_iso8601(date):
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4] + 'Z'


def check_time_intervals(working_hours, delivery_hours):
    for work in working_hours:
        for delivery in delivery_hours:
            work_time = serializers.TimeInterval(work)
            delivery_time = serializers.TimeInterval(delivery)
            if not (delivery_time.end < work_time.start or work_time.end < delivery_time.start):
                return True
    return False


def get_rating(courier):
    try:
        if not courier.order_set.filter(complete_time__isnull=False).count():
            return
        regions = courier.regions
        delivery_time_regions = []
        for region in regions:
            delivery_times = []
            orders_completed = courier.order_set.filter(complete_time__isnull=False, region=region) \
                .order_by("complete_time")
            if not orders_completed.count():
                continue
            delivery_times.append(
                (orders_completed[0].complete_time - orders_completed[0].assign_time).total_seconds()
            )
            for order_index in range(1, len(orders_completed)):
                delivery_times.append(
                    (orders_completed[order_index].complete_time - orders_completed[
                        order_index - 1].complete_time).total_seconds()
                )
            delivery_time_regions.append((sum(delivery_times) / len(delivery_times)))
        minimal = min(delivery_time_regions)
        print(minimal)
        return (60 * 60 - min(minimal, 60 * 60)) / (60 * 60) * 5
    except Exception as e:
        raise Exception(e)


def get_earnings(courier):
    orders_completed_count = courier.order_set.filter(complete_time__isnull=False).count()
    if not orders_completed_count:
        return 0
    return orders_completed_count * (500 * convert_courier_type_to_coef(courier.courier_type))
