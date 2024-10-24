from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.billable_metric import (
    BillableMetricEvaluateExpression,
    BillableMetricEvaluateExpressionResponse,
    BillableMetricResponse,
)
from ..services.request import make_headers, make_url, send_post_request
from ..services.response import Response, prepare_object_response, get_response_data


class BillableMetricClient(
    CreateCommandMixin[BillableMetricResponse],
    DestroyCommandMixin[BillableMetricResponse],
    FindAllCommandMixin[BillableMetricResponse],
    FindCommandMixin[BillableMetricResponse],
    UpdateCommandMixin[BillableMetricResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "billable_metrics"
    RESPONSE_MODEL: ClassVar[Type[BillableMetricResponse]] = BillableMetricResponse
    ROOT_NAME: ClassVar[str] = "billable_metric"

    def evaluate_expression(
        self, input_object: BillableMetricEvaluateExpression
    ) -> BillableMetricEvaluateExpressionResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, "evaluate_expression"),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=BillableMetricEvaluateExpressionResponse,
            data=get_response_data(response=api_response, key="expression_result"),
        )
