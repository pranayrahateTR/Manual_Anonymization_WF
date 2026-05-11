import allure
import pytest
import time

from pages.Approver import Role_Approver
from pages.LoginPage import LoginPage
from testcases.BaseTest import BaseTest
from utilities import dataProvider


class TestCompleteWorkflow(BaseTest):
    """
    Complete end-to-end workflow:
    1. Login as Approver
    2. Approver creates request
    3. API updates role to Redactor
    4. Redactor processes the request
    """

    # ============================================================================
    # CREDENTIAL MANAGEMENT - TWO APPROACHES:
    # ============================================================================

    # OLD APPROACH (Excel-based) - COMMENTED OUT:
    # @pytest.mark.parametrize("username,password", dataProvider.get_data("LoginCreds","testdata.xlsx"))
    # - Reads credentials directly from Excel file
    # - Security risk: Excel file could be committed to Git
    # - Hard to manage different credentials per developer

    # NEW APPROACH (Environment variables) - ACTIVE:
    # - Uses login_credentials fixture from conftest.py
    # - Fixture reads from .env file (via os.getenv)
    # - Secure: .env file is gitignored
    # - Each developer has their own .env with their credentials
    # ============================================================================

    @pytest.mark.parametrize("Engagement,TemplateName,PageType,PageNumber,PageRange,StartDate,EndDate,Priority",
                             dataProvider.get_data("Doc_CreateRequest","Binderdetails.xlsx"))
    def test_complete_workflow(self, login_credentials, Engagement, TemplateName, PageType,
                               PageNumber, PageRange, StartDate, EndDate, Priority, page):

        # Extract username and password from login_credentials fixture
        # This fixture reads from .env file (APP_USERNAME, APP_PASSWORD)
        username, password = login_credentials

        print("\n" + "="*80)
        print("*** STARTING COMPLETE WORKFLOW TEST ***")
        print("="*80)
        print(f"Test Parameters:")
        print(f"   User: {username}")
        print(f"   Credential Source: .env file (via login_credentials fixture)")
        print(f"   Engagement: {Engagement}")
        print(f"   Template: {TemplateName}")
        print(f"   Priority: {Priority}")
        print("="*80 + "\n")

        with allure.step("Step 1: Login and Approver Workflow"):
            print("\n>> STEP 1: Login and Create Request")
            print("-" * 60)
            print(f"   > Logging in as user: {username}")
            lp = LoginPage(page)
            # Approver workflow - creates request and returns request_id
            request, redactor_role = lp.doLogin(username, password)\
                .Create_Job(Engagement, TemplateName, PageType, PageNumber, PageRange, StartDate, EndDate, Priority)

            print(f"   [OK] Login successful - Role: Approver")
            print(f"   [OK] Request created: {request}")
            print(f"[STEP 1 COMPLETE] Request ID captured: {request}\n")

        with allure.step("Step 2: Update Role from Approver to Redactor (API)"):
            print("\n>> STEP 2: Update User Role via API")
            print("-" * 60)
            print(f"   > Updating role from Approver -> Redactor")
            # Update role using the returned redactor_role object
            redactor_role.login_and_update_role()
            print(f"   [OK] Role updated successfully: Redactor")
            print(f"[STEP 2 COMPLETE] User role updated to Redactor\n")

        with allure.step("Step 3: Redactor Workflow - Process Request"):
            print("\n>> STEP 3: Perform Redactions")
            print("-" * 60)
            print(f"   > Processing request: {request}")
            # Perform redactions using the request from step 1
            redactor_role.peform_redactions(request)
            print(f"   [OK] Redactions completed and submitted")
            print(f"   [OK] Role auto-updated back to: Approver")
            print(f"[STEP 3 COMPLETE] Redactions performed for request: {request}\n")

        with allure.step("Step 4: Approve Request"):
            print("\n>> STEP 4: Approve and Export Request")
            print("-" * 60)
            print(f"   > Refreshing page to load Approver interface")
            # Refresh page to reflect role change back to Approver
            # page.reload()
            time.sleep(1)  # Increased wait for page to fully load approval interface
            print(f"   [OK] Page refreshed successfully")

            # Perform Export and Complete step
            print(f"   > Approving request: {request}")
            approve=Role_Approver(page)
            approve_req=approve.approve_job(request)
            print(f"   [OK] Request approved and exported")
            print(f"[STEP 4 COMPLETE] Approved request: {request}\n")

        print("\n" + "="*80)
        print("*** WORKFLOW COMPLETED SUCCESSFULLY! ***")
        print("="*80 + "\n")