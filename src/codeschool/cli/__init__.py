"""
The command line interface app offers endpoints for consumption by
the `codeschool` and `codeschoolclt` programs.

All these endpoints are based on a JSON-RPC
"""
default_app_config = 'codeschool.cli.apps.CliConfig'

from jsonrpc.backend.django import JSONRPCAPI

api = JSONRPCAPI()
