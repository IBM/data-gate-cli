#  Copyright 2020 IBM Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from dg.lib.cluster.cluster import AbstractCluster
from dg.lib.cluster.cluster_factory import AbstractClusterFactory, ClusterData
from dg.lib.ibmcloud.cluster.ibmcloud_cluster import IBMCloudCluster


class IBMCloudClusterFactory(AbstractClusterFactory):
    def create_cluster(self, server: str, cluster_data: ClusterData) -> AbstractCluster:
        return IBMCloudCluster(server, cluster_data)


ibm_cloud_cluster_factory = IBMCloudClusterFactory()
