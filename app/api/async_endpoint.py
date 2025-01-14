# app/api/async_endpoint.py
import asyncio

from flask_restx import Namespace, Resource

async_ns = Namespace('async-demo', description="Demo Async Endpoint")


@async_ns.route('/hello')
class AsyncHelloResource(Resource):
    async def get(self):
        """
        An asynchronous endpoint demo.
        Note: True async support in Flask 2.0+ is limited.
        This example uses 'async def', but concurrency is
        managed by the server (e.g., gevent or eventlet).
        """
        # Simulate some async work
        await asyncio.sleep(1)
        return {"message": "Hello from async endpoint!"}, 200
