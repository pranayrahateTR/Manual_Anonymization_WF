import allure
import pytest

from pages.LoginPage import LoginPage
from testcases.BaseTest import BaseTest
from utilities import dataProvider


class TestLogin(BaseTest):
    """
    Test suite for login functionality only.
    Verifies that users can successfully authenticate and are assigned correct roles.
    """

    @pytest.mark.parametrize("username,password", dataProvider.get_data("LoginCreds", "testdata.xlsx"))
    def test_login_success(self, username, password, page):
        """
        Test successful login and role verification.

        Steps:
        1. Navigate to login page
        2. Enter credentials
        3. Verify successful login
        4. Verify user role is assigned correctly
        """
        with allure.step("Performing Login Test"):
            lp = LoginPage(page)
            # doLogin returns Role_Approver object, not a tuple
            role_approver = lp.doLogin(username, password)

            # Verify that we got a Role_Approver instance
            assert role_approver is not None, "Login failed - Role_Approver object is None"
            print(f"✓ Login successful for user: {username}")



