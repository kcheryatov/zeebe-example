# https://flask-restx.readthedocs.io/en/latest/swagger.html#documenting-the-fields
# https://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/

import datetime
import json
import uuid
import logging

from flask import Flask
from flask_restx import Api, Resource, fields, reqparse

import defaults
from create_order_kafka_event_producer import CreateOrderKafkaProducer


app = Flask(__name__)
api = Api(app, version='1.0', title='Order open api',
          description='Order open api')

order_item_model = api.model('OrderItem', {
    'product_offering_id': fields.String(required=True, description='Product offering identifier')
})
payment_model = api.model('Payment', {
    'payment_type': fields.String(required=True, description='Type of payment: card or account'),
    'transaction_id': fields.String(required=True, description='Payment transaction identifier')
})
order_model = api.model('Order', {
    'client_id': fields.String(required=True, description='client identifier'),
    'payment': fields.Nested(payment_model, required=True),
    'items': fields.List(fields.Nested(order_item_model), required=True)
})
ns_order = api.namespace('orders', description='Operations related to orders')


@ns_order.route('/order/submit')
class Orders(Resource):

    @api.expect(order_model, validate=True)
    def post(self):
        """Post new order"""
        order = json.loads(reqparse.request.data.decode("utf-8"))

        order["id"] = str(uuid.uuid4())
        order["status"] = "new"
        order["version_date"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        for i in range(len(order["items"])):
            order["items"][i]["local_id"] = i
            order["items"][i]["status"] = "new"

        try:
            CreateOrderKafkaProducer().send_message(order)
            return order, 202
        except Exception as ex:
            logging.error("Process order failed {}".format(ex))
            return ex, 500


if __name__ == '__main__':
    app.run(debug=True)
