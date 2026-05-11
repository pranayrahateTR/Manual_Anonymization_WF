import allure
import pytest

from testcases.BaseTest import BaseTest
from utilities import dataProvider


class TestApproverRole(BaseTest):
    """
    Test suite for Approver role functionality.
    Tests document search, request creation, and approver-specific workflows.
    Assumes user is already logged in as Approver (via logged_in_approver fixture).
    """

    @pytest.mark.parametrize("Engagement,TemplateName,PageType,PageNumber,PageRange,StartDate,EndDate,Priority",
                             dataProvider.get_data("Doc_CreateRequest", "Binderdetails.xlsx"))
    def test_approver_create_request(self, Engagement, TemplateName, PageType, PageNumber, PageRange,
                                      StartDate, EndDate, Priority, logged_in_approver):
        """
        Test Approver workflow: Create a redaction request.

        Steps:
        1. Navigate to document search (using logged-in Approver session)
        2. Enter search criteria
        3. Select documents
        4. Create redaction request
        5. Capture and verify request ID

        Returns:
            tuple: (request_id, Redactor_Role object) for downstream workflow
        """
        with allure.step("Step 1: Create Redaction Request as Approver"):
            # Use the logged_in_approver fixture (already authenticated)
            role_approver = logged_in_approver

            # Execute Approver workflow: creates request and returns request_id + Redactor_Role
            request, redactor_role = role_approver.Approver_role(
                Engagement, TemplateName, PageType, PageNumber, PageRange,
                StartDate, EndDate, Priority
            )

            print(f"✓ Request created successfully. Request ID: {request}")

            # Store for potential use in other tests
            return request, redactor_role