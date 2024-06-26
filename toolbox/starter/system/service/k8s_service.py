"""K8s domain service interface"""

from abc import ABC

from toolbox.starter.system.schema.k8s_schema import K8sInitCmd
from toolbox.starter.system.service.base_deploy_service import BaseDeployService


class K8sService(BaseDeployService, ABC):
    async def k8s_init(self, k8sInitCmd: K8sInitCmd): ...
