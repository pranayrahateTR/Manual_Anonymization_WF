import allure
import pytest

from pages.Redactor import Redactor_Role
from testcases.BaseTest import BaseTest
from utilities import dataProvider


class TestRedactorRole(BaseTest):
    """
    Test suite for Redactor role functionality.
    Tests role update and redaction operations.
    Note: This test updates user role via API and performs redactions.
    """

    @pytest.mark.parametrize("request_id", [("12345",)])  # You can replace with actual request IDs or fetch from DB
    def test_redactor_workflow(self, page, request_id):
        """
        Test Redactor workflow: Update role and perform redactions.

        Steps:
        1. Update user role from Approver to Redactor (via API)
        2. Refresh browser session to get new role
        3. Perform redactions on the specified request

        Args:
            request_id: The request ID to process (can be from previous Approver test)
        """
        with allure.step("Step 1: Update user role to Redactor via API"):
            redactor = Redactor_Role(page)
            redactor.login_and_update_role()
            print(f"✓ User role updated to Redactor")

        with allure.step("Step 2: Perform redactions on request {request_id}"):
            redactor.peform_redactions(request_id)
            print(f"✓ Redactions completed for request: {request_id}")
