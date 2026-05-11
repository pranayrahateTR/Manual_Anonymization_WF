import time

from pages.Approver import Role_Approver
from pages.BasePage import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username = None  # Initialize
        self.user_role = None


    def doLogin(self, username, password):
        self.username = username  # Store for later use

        self.type("An_username", str(username))
        self.type("An_password", str(password))
        self.click("An_SignOnBtn")
        self.wait_for_load_state("networkidle")
        time.sleep(15)

        self.verifyRole()  # Call verify after login

        return Role_Approver(self.page)

    def verifyRole(self):
        # Wait for role element to have text (retry up to 10 times)
        import time
        for attempt in range(10):
            self.user_role = self.get_text("An_userRole")
            if self.user_role and self.user_role.strip():
                break
            time.sleep(1)
        else:
            raise AssertionError(f"Role element remained empty after 10 seconds")

        if self.user_role == "(Approver)":
            print(f"[OK] User '{self.username}' logged in as Approver")

        elif self.user_role == "(Redactor)":
            print(f"[ERROR] User '{self.username}' is Redacter, not Approver. Logging out...")
            self.logout()
            raise AssertionError(f"User '{self.username}' has role '{self.user_role}', expected 'Approver'")

        else:
            raise AssertionError(f"Unknown role '{self.user_role}' for user '{self.username}'")
