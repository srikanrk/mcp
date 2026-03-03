# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""AgentCore Runtime MCP server for AWS Data Processing.

Deploys the aws-dataprocessing-mcp-server as a remote MCP server
on Amazon Bedrock AgentCore Runtime using streamable-http transport.
"""

import os

from mcp.server.fastmcp import FastMCP


# Server configuration
SERVER_INSTRUCTIONS = """AWS Data Processing MCP Server - Remote deployment on AgentCore Runtime.
Provides tools for managing AWS Glue, EMR, and Athena resources."""

SERVER_DEPENDENCIES = [
    'pydantic>=2.10.6',
    'loguru>=0.7.0',
    'boto3>=1.34.0',
    'requests>=2.31.0',
    'pyyaml>=6.0.0',
    'cachetools>=5.3.0',
]

# Create FastMCP server configured for AgentCore (stateless HTTP on 0.0.0.0)
mcp = FastMCP(
    'awslabs.aws-dataprocessing-mcp-server',
    instructions=SERVER_INSTRUCTIONS,
    dependencies=SERVER_DEPENDENCIES,
    host='0.0.0.0',
    stateless_http=True,
)

# Read config from environment
allow_write = os.environ.get('ALLOW_WRITE', 'true').lower() == 'true'
allow_sensitive = os.environ.get('ALLOW_SENSITIVE_DATA_ACCESS', 'false').lower() == 'true'

# Register all handlers
from awslabs.aws_dataprocessing_mcp_server.handlers.glue.data_catalog_handler import (
    GlueDataCatalogHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.glue.interactive_sessions_handler import (
    GlueInteractiveSessionsHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.glue.worklows_handler import (
    GlueWorkflowAndTriggerHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.glue.glue_etl_handler import (
    GlueEtlJobsHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.glue.glue_commons_handler import (
    GlueCommonsHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.glue.crawler_handler import (
    CrawlerHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.athena.athena_query_handler import (
    AthenaQueryHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.athena.athena_data_catalog_handler import (
    AthenaDataCatalogHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.athena.athena_workgroup_handler import (
    AthenaWorkGroupHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.emr.emr_ec2_cluster_handler import (
    EMREc2ClusterHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.emr.emr_ec2_steps_handler import (
    EMREc2StepsHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.emr.emr_ec2_instance_handler import (
    EMREc2InstanceHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.emr.emr_serverless_application_handler import (
    EMRServerlessApplicationHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.emr.emr_serverless_job_run_handler import (
    EMRServerlessJobRunHandler,
)
from awslabs.aws_dataprocessing_mcp_server.handlers.commons.common_resource_handler import (
    CommonResourceHandler,
)


GlueDataCatalogHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
GlueInteractiveSessionsHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
GlueWorkflowAndTriggerHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
GlueEtlJobsHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
GlueCommonsHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
CrawlerHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
AthenaQueryHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
AthenaDataCatalogHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
AthenaWorkGroupHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
EMREc2ClusterHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
EMREc2StepsHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
EMREc2InstanceHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
EMRServerlessApplicationHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
EMRServerlessJobRunHandler(mcp, allow_write=allow_write, allow_sensitive_data_access=allow_sensitive)
CommonResourceHandler(mcp, allow_write=allow_write)


if __name__ == '__main__':
    mcp.run(transport='streamable-http')
