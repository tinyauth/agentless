from flask import jsonify, request
from flask_restful import Resource, abort, fields, marshal, reqparse

from agentless.app import api, db
from agentless.models import PrivateKey
from agentless.simplerest import build_response_for_request

private_key_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'public_key': fields.String,
}

private_key_parser = reqparse.RequestParser()
private_key_parser.add_argument('name', type=str, location='json', required=True)


class PrivateKeyResource(Resource):

    def _get_or_404(self, private_key_id):
        private_key = PrivateKey.query.filter(PrivateKey.id == private_key_id).first()
        if not private_key:
            abort(404, message=f'private_key {private_key_id} does not exist')
        return private_key

    def get(self, private_key_id):
        private_key = self._get_or_404(private_key_id)
        return jsonify(marshal(private_key, private_key_fields))

    def put(self, private_key_id):
        private_key = self._get_or_404(private_key_id)

        args = private_key_parser.parse_args()

        private_key.name = args['name']

        db.session.add(private_key)

        db.session.commit()

        return jsonify(marshal(private_key, private_key_fields))

    def delete(self, private_key_id):
        private_key = self._get_or_404(private_key_id)
        db.session.delete(private_key)

        return '{}', 201


class PrivateKeysResource(Resource):

    def get(self):
        return build_response_for_request(PrivateKey, request, private_key_fields)

    def post(self):
        args = private_key_parser.parse_args()

        private_key = PrivateKey(
            name=args['name'],
        )

        db.session.add(private_key)
        db.session.commit()

        return jsonify(marshal(private_key, private_key_fields))


api.add_resource(PrivateKeysResource, '/keys')
api.add_resource(PrivateKeyResource, '/keys/<key_id>')
