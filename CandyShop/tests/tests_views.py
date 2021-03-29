from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from CandyShop.models import Order, Courier
import datetime
from CandyShop import custom_functions


class OrderTest(APITestCase):
    def setUp(self):
        self.correct_error_response_template = \
            {
                "validation_error": {
                    "orders": [

                    ]
                },
                "errors": {
                    "data": [

                    ]
                }
            }
        self.correct_post_data = \
            {
                "data": [
                    {
                        "order_id": 3,
                        "weight": 0.23,
                        "region": 12,
                        "delivery_hours": ["09:00-18:00"]
                    },
                    {
                        "order_id": 4,
                        "weight": 15,
                        "region": 1,
                        "delivery_hours": ["09:00-18:00"]
                    },
                    {
                        "order_id": 5,
                        "weight": 0.01,
                        "region": 22,
                        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                    }
                ]
            }
        self.orders = []
        self.orders.append({"order_id": 1, "region": 1, "weight": 15, "delivery_hours": ["23:59-23:59"]})
        self.orders.append({"order_id": 2, "region": 2, "weight": 40, "delivery_hours": ["00:00-23:00", "23:23-23:25"]})
        for order in self.orders:
            Order.objects.create(**order)

    def test_get_orders_list(self):
        url = reverse('orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.orders)

    def test_post_orders_list_correct(self):
        url = reverse('orders-list')

        response = self.client.post(url, self.correct_post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {"orders": [{"id": i.get("order_id")} for i in self.correct_post_data.get("data")]})

    def test_post_orders_list_incorrect_order_id(self):
        url = reverse('orders-list')
        incorrect_data = self.correct_post_data
        incorrect_data['data'][0]['order_id'] = 1

        response = self.client.post(url, incorrect_data, format="json")
        correct_response = self.correct_error_response_template
        correct_response['validation_error']['orders'].append({"id": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('validation_error') is not None, True)
        self.assertEqual(response.data.get('validation_error'), correct_response['validation_error'])

    def test_post_orders_list_incorrect_weight(self):
        url = reverse('orders-list')
        incorrect_data = self.correct_post_data
        incorrect_data['data'][0]['weight'] = 50.01
        incorrect_data['data'][1]['weight'] = 0.001

        response = self.client.post(url, incorrect_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        correct_response = self.correct_error_response_template
        correct_response['validation_error']['orders'].extend([{"id": 3}, {"id": 4}])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('validation_error') is not None, True)
        self.assertEqual(response.data.get('validation_error'), correct_response['validation_error'])

    def test_post_orders_list_incorrect_region(self):
        url = reverse('orders-list')
        incorrect_data = self.correct_post_data
        incorrect_data['data'][0]['region'] = 'k3k1n6'

        response = self.client.post(url, incorrect_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        correct_response = self.correct_error_response_template
        correct_response['validation_error']['orders'].append({"id": 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('validation_error') is not None, True)
        self.assertEqual(response.data.get('validation_error'), correct_response['validation_error'])

    def test_post_orders_list_incorrect_delivery_hours(self):
        url = reverse('orders-list')
        incorrect_data = self.correct_post_data
        incorrect_data['data'][0]['delivery_hours'] = []
        incorrect_data['data'][1]['delivery_hours'] = ["23:00-01:00"]
        incorrect_data['data'][2]['delivery_hours'] = ["23:00-23:23", "23:00-23:69"]

        response = self.client.post(url, incorrect_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        correct_response = self.correct_error_response_template
        correct_response['validation_error']['orders'].extend([{"id": 3}, {"id": 4}, {"id": 5}])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('validation_error') is not None, True)
        self.assertEqual(response.data.get('validation_error'), correct_response['validation_error'])


class CourierTest(APITestCase):
    def setUp(self):
        self.correct_post_data = \
            {
                "data": [
                    {
                        "courier_id": 3,
                        "courier_type": "foot",
                        "regions": [
                            1,
                            12,
                            22
                        ],
                        "working_hours": [
                            "11:35-14:05",
                            "09:00-11:00"
                        ]
                    },
                    {
                        "courier_id": 4,
                        "courier_type": "bike",
                        "regions": [
                            22
                        ],
                        "working_hours": [
                            "09:00-18:00"
                        ]
                    },
                    {
                        "courier_id": 5,
                        "courier_type": "car",
                        "regions": [
                            12,
                            22,
                            23,
                            33
                        ],
                        "working_hours": []
                    }
                ]
            }
        self.correct_error_response_template = \
            {
                "validation_error": {
                    "couriers": [

                    ]
                },
                "errors": {
                    "data": [

                    ]
                }
            }
        self.couriers = []
        self.couriers.append(
            {"courier_id": 1, "courier_type": 'foot', "regions": [1, 2, 3], "working_hours": ["00:00-10:00"]})
        self.couriers.append(
            {"courier_id": 2, "courier_type": 'bike', "regions": [2], "working_hours": ["10:00-16:00", "19:00-21:00"]})
        for courier in self.couriers:
            Courier.objects.create(**courier)

    def test_get_couriers_list(self):
        url = reverse('couriers-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.couriers)

    def test_post_couriers_list_correct(self):
        url = reverse('couriers-list')

        response = self.client.post(url, self.correct_post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {"couriers": [{"id": i.get("courier_id")} for i in self.correct_post_data.get("data")]})

    def test_post_couriers_list_incorrect_order_id(self):
        url = reverse('couriers-list')
        incorrect_data = self.correct_post_data
        incorrect_data['data'][0]['courier_id'] = 1

        response = self.client.post(url, incorrect_data, format="json")
        correct_response = self.correct_error_response_template
        correct_response['validation_error']['couriers'].append({"id": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('validation_error') is not None, True)
        self.assertEqual(response.data.get('validation_error'), correct_response['validation_error'])

    def test_post_couriers_list_incorrect_courier_type(self):
        url = reverse('couriers-list')
        incorrect_data = self.correct_post_data
        incorrect_data['data'][0]['courier_type'] = 'k3k1n6'
        incorrect_data['data'][1]['courier_type'] = 125

        response = self.client.post(url, incorrect_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        correct_response = self.correct_error_response_template
        correct_response['validation_error']['couriers'].extend([{"id": 3}, {"id": 4}])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('validation_error') is not None, True)
        self.assertEqual(response.data.get('validation_error'), correct_response['validation_error'])

    def test_post_couriers_list_incorrect_region(self):
        url = reverse('couriers-list')
        incorrect_data = self.correct_post_data
        incorrect_data['data'][0]['regions'] = ["asd", "asf"]
        incorrect_data['data'][1]['regions'] = 1
        incorrect_data['data'][2]['regions'] = []

        response = self.client.post(url, incorrect_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        correct_response = self.correct_error_response_template
        correct_response['validation_error']['couriers'].extend([{"id": 3}, {"id": 4}, {"id": 5}])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('validation_error') is not None, True)
        self.assertEqual(response.data.get('validation_error'), correct_response['validation_error'])

    def test_post_couriers_list_incorrect_working_hours(self):
        url = reverse('couriers-list')

        incorrect_data = self.correct_post_data
        incorrect_data['data'][0]['working_hours'] = ["23:00-01:00"]
        incorrect_data['data'][1]['working_hours'] = ["23:00-23:23", "23:00-23:69"]

        response = self.client.post(url, incorrect_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        correct_response = self.correct_error_response_template
        correct_response['validation_error']['couriers'].extend([{"id": 3}, {"id": 4}])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('validation_error') is not None, True)
        self.assertEqual(response.data.get('validation_error'), correct_response['validation_error'])

    def test_post_couriers_detail(self):
        pass


class AssignCompleteRatingEarningsTest(APITestCase):
    def setUp(self):
        self.orders = []
        # suitable region for car
        self.orders.append(
            {"order_id": 1, "region": 4, "weight": 9, "delivery_hours": ["00:00-23:59"]})
        # suitable weight for car
        self.orders.append(
            {"order_id": 2, "region": 4, "weight": 41, "delivery_hours": ["00:00-16:00", "23:23-23:25"]})
        # unsuitable time for both couriers
        self.orders.append(
            {"order_id": 3, "region": 3, "weight": 0.01, "delivery_hours": ["11:00-19:00"]})
        # suitable for foot
        self.orders.append(
            {"order_id": 4, "region": 2, "weight": 5.01, "delivery_hours": ["23:00-23:30", "9:00-11:00"]})
        # suitable for foot
        self.orders.append(
            {"order_id": 5, "region": 1, "weight": 4.70, "delivery_hours": ["04:00-10:00"]})
        # suitable for foot (but cannot be assigned with previous orders
        self.orders.append(
            {"order_id": 6, "region": 2, "weight": 5.02, "delivery_hours": ["08:00-09:00"]}
        )
        for order in self.orders:
            Order.objects.create(**order)

        self.couriers = []
        self.couriers.append(
            {"courier_id": 1, "courier_type": 'foot', "regions": [1, 2, 3], "working_hours": ["06:00-10:00"]})
        self.couriers.append(
            {"courier_id": 2, "courier_type": 'car', "regions": [4], "working_hours": ["10:00-15:00", "19:00-21:00"]})
        self.couriers.append(
            {"courier_id": 3, "courier_type": 'bike', "regions": [5], "working_hours": []}
        )
        for courier in self.couriers:
            Courier.objects.create(**courier)

    def test_post_orders_assign_foot_courier(self):
        url = reverse("orders-assign")
        data = {"courier_id": self.couriers[0].get("courier_id")}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("orders"), [{"id": 4}, {"id": 5}])
        self.assertEqual(response.data.get("assign_time") is not None, True)

    def test_post_orders_assign_car_courier(self):
        url = reverse("orders-assign")
        data = {"courier_id": self.couriers[1].get("courier_id")}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("orders"), [{"id": 1}, {"id": 2}])
        self.assertEqual(response.data.get("assign_time") is not None, True)

    def test_post_orders_assign_twice_foot_courier(self):
        url_assign = reverse("orders-assign")
        url_complete = reverse("orders-complete")

        data_assign = {"courier_id": self.couriers[0].get("courier_id")}
        response = self.client.post(url_assign, data_assign, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("orders"), [{"id": 4}, {"id": 5}])
        self.assertEqual(response.data.get("assign_time") is not None, True)

        data_complete = data_assign.copy()
        data_complete.update(
            {
                "order_id": 4,
                "complete_time":
                    custom_functions.convert_datetime_to_iso8601(
                        datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                    )
            })

        response = self.client.post(url_complete, data_complete, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"order_id": 4})

        response = self.client.post(url_assign, data_assign, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("orders"), [{"id": 5}, {"id": 6}])
        self.assertEqual(response.data.get("assign_time") is not None, True)

    def test_post_orders_assign_bike_courier(self):
        url = reverse("orders-assign")
        data = {"courier_id": self.couriers[2].get("courier_id")}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("orders"), [])
        self.assertEqual(response.data.get("assign_time") is None, True)

    def test_post_orders_complete_incorrect(self):
        url = reverse("orders-assign")
        data = {"courier_id": self.couriers[1].get("courier_id")}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("orders"), [{"id": 1}, {"id": 2}])
        self.assertEqual(response.data.get("assign_time") is None, False)

        url_complete = reverse("orders-complete")
        data_complete = {
            "order_id": 4,
            "complete_time":
                custom_functions.convert_datetime_to_iso8601(
                    datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                )
        }
        data_complete.update(data)
        response = self.client.post(url_complete, data_complete, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("order_id") is not None, True)
