import time

from pages.BasePage import BasePage
# Import from sibling directory using relative import from parent
#from Anonymization_api.test_userlogin import perform_login, update_user_role
from utilities import configReader


class Redactor_Role(BasePage):
    def __init__(self, page):
        super().__init__(page)


    def login_and_update_role(self, credentials=None, user_data=None):
        """
        Update user role using subprocess (separate process - no browser interference)

        Args:
            credentials: Not used (kept for compatibility)
            user_data: Not used (kept for compatibility)

        Returns:
            self for method chaining
        """
        import subprocess
        import sys
        from pathlib import Path

        # Path to the API updater script
        script_path = Path(__file__).parent.parent / "Anonymization_api" / "api_role_updater.py"

        print("Updating user role via API (separate process)...")

        # Run the API script in a SEPARATE Python process
        # This completely isolates it from the browser session
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Print output from the subprocess
        if result.stdout:
            print(result.stdout)

        # Check if the subprocess succeeded
        if result.returncode == 0:
            print("[OK] Role update completed successfully (via subprocess)")
        else:
            error_msg = result.stderr if result.stderr else "Unknown error"
            raise Exception(f"Role update failed: {error_msg}")

        return self

    def update_role_to_approver(self):
        """
        Update user role from Redactor back to Approver via API
        Called after redaction submission to complete the workflow

        Returns:
            self for method chaining
        """
        import subprocess
        import sys
        from pathlib import Path

        # Path to the Approver API updater script
        script_path = Path(__file__).parent.parent / "Anonymization_api" / "api_role_updater_approver.py"

        print("Updating user role to Approver via API (separate process)...")

        # Run the API script in a SEPARATE Python process
        result = subprocess.run(
            [sys.executable, str(script_path)], # USer Role is updated to Redactor
            capture_output=True,
            text=True,
            timeout=30
        )

        # Print output from the subprocess
        if result.stdout:
            print(result.stdout)

        # Check if the subprocess succeeded
        if result.returncode == 0:
            print("[OK] Role update to Approver completed successfully")
        else:
            error_msg = result.stderr if result.stderr else "Unknown error"
            raise Exception(f"Role update to Approver failed: {error_msg}")

        return self

    # def get_auth_token(self, credentials=None):
    #     """
    #     Just get the authentication token without updating role
    #
    #     Args:
    #         credentials: Login credentials (optional)
    #
    #     Returns:
    #         str: Authentication token
    #     """
    #     return perform_login(credentials)

    time.sleep(5)
    def peform_redactions(self,request):

        print(f"\n      ** Redactor.peform_redactions() - Starting redaction workflow")

        print(f"      > Refreshing page (1st refresh)")
        self.refresh_page()
        time.sleep(3)

        # Debug: Print the request ID we're using
        print(f"      > Using Request GUID: {request}")
        print(f"         • Type: {type(request)}")

        # Wait for the field to be ready
        time.sleep(2)

        print(f"      > Entering GUID in search field")
        # Use the config-based type method with the new CSS selector
        self.type("An_group_id_field", request)
        print(f"      [OK] GUID entered successfully")

        time.sleep(2)

        print(f"      > Clicking 'Assign' button")
        self.click_by_text("An_Assign_btn")
        time.sleep(3)  # Wait for confirmation dialog to appear

        print(f"      > Confirming assignment (clicking 'Yes')")
        self.click("An_Assign_Yes_btn")
        self.handle_alert()
        time.sleep(2)

        print(f"      > Opening 'Redaction Pending' view")
        self.click("An_Redaction_Pending_btn")
        time.sleep(8)

        print(f"      > Entering full screen mode")
        self.click("An_Approver_Enter_FullScreen_btn")

        print(f"      > Testing zoom controls")
        self.click("An_Zoom_In")
        time.sleep(1)
        for i in range(5):
            self.click("An_Zoom_Out")

        print(f"      > Drawing redaction box (Payer's Name area)")
        # ============================================================
        # DRAW REDACTION BOXES — app internal coordinates
        # ============================================================

        # DEBUG: Log canvas info to compare with standalone script
        canvas_selector = configReader.readConfig("locators", "An_redaction_box")
        info = self.get_canvas_info(canvas_selector)
        print(f"      > CANVAS DEBUG: rectX={info['rectX']:.1f}, rectY={info['rectY']:.1f}")
        print(f"      > CANVAS DEBUG: rectW={info['rectWidth']:.1f}, rectH={info['rectHeight']:.1f}")
        print(f"      > CANVAS DEBUG: native={info['nativeWidth']}x{info['nativeHeight']}")
        print(f"      > CANVAS DEBUG: scale={info['scale']}")
        print(f"      > Drawing redaction boxes on PII fields")

        # 1. Payer name + address (UNITED BANK AND TRUST, P O BOX 130, DURANT OK)
        self.drag_redaction_box('An_redaction_box', 220, 250, 750, 450)
        time.sleep(1)

        # 2. Payer's TIN (73-0222372)
        self.drag_redaction_box('An_redaction_box', 220, 630, 490, 690)
        time.sleep(1)

        # 3. Recipient's TIN (111-11-1111)
        self.drag_redaction_box('An_redaction_box', 740, 630, 1000, 690)
        time.sleep(1)

        # 4. Recipient's name (JACK ANDERSON)
        self.drag_redaction_box('An_redaction_box', 220, 810, 680, 870)
        time.sleep(1)

        # 5. Street address (1234 MAIN STREET,)
        self.drag_redaction_box('An_redaction_box', 225, 960, 700, 1020)
        time.sleep(1)


        # 6. City/State/ZIP (NEWPORT BEACH, CA 92660)
        self.drag_redaction_box('An_redaction_box', 220, 1160, 760, 1110)

        time.sleep(3)

        print(f"      > Saving redaction")
        self.click_by_text("An_redaction_save_btn")


        time.sleep(2)
        print(f"      > Handling save confirmation alert")
        self.handle_alert()
        time.sleep(2)

        print(f"      > Exiting full screen mode")
        self.click("An_Approver_Exit_FullScreen_btn")
        time.sleep(1)

        print(f"      > Submitting redactions for review")
        self.click_by_text("An_redaction_Submit")
        time.sleep(2)

        print(f"      > Handling submission confirmation alert")
        self.handle_alert()
        time.sleep(2)

        print(f"      > Navigating to Home tab")
        # Use role-based selector to avoid ambiguity with multiple "Home" elements
        self.click("An_Redactor_HomeTab")

        # Update role back to Approver after redaction submission
        print(f"\n      > ROLE UPDATE: Switching from Redactor > Approver")
        self.update_role_to_approver()
        time.sleep(4)  # Wait for role update to propagate (API takes ~3 seconds)

        print(f"      > Refreshing page after role update")
        self.refresh_page()
        print(f"      [OK] Role updated to Approver successfully")

        print(f"      > Final wait for role propagation")
        time.sleep(4)  # Wait for role update to propagate (API takes ~3 seconds)

        print(f"      [OK] Redaction workflow completed successfully\n")
        return self














