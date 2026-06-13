import time

from pages.BasePage import BasePage
from pages.Redactor import Redactor_Role
from utilities import dataProvider
from utilities.dataProvider import get_data

class Role_Approver(BasePage):

    def __init__(self, page):
        super().__init__(page)


    def Create_Job(self, Engagement, TemplateName, PageType, PageNumber, PageRange, StartDate, EndDate, Priority):

        print(f"\n      ** Approver.Create_Job() - Creating new anonymization request")
        print(f"      > Parameters: Engagement={Engagement}, Template={TemplateName}, Priority={Priority}")

        print(f"      > Navigating to Request tab")
        self.click_by_text("An_requesttab")

        print(f"      > Opening Document Search")
        self.click_by_text("An_DocumentSearch")

        print(f"      > Filling search criteria:")
        self.type("An_engagementId",str(Engagement))
        print(f"         • Engagement ID: {Engagement}")
        self.type("An_templateName",TemplateName)
        print(f"         • Template Name: {TemplateName}")
        self.type("An_pageType",PageType)
        self.type("An_pageNumber",str(PageNumber))
        self.type("An_pageRange",PageRange)
        print(f"         • Page Range: {PageRange}")
        self.type("An_startDate",StartDate)
        self.type("An_endDate",EndDate)

        print(f"      > Clicking Search button")
        self.click_by_text("An_searchBtn")
        time.sleep(2)

        print(f"      > Setting priority to: {Priority}")
        self.select_dropdown_by_label("An_priorityDrpdown",Priority)

        print(f"      > Selecting all documents")
        self.click_by_text("An_selectAllcheckbox")

        print(f"      > Selecting ManualAnonymizationRequest")
        self.click_by_text("An_manualAnonymizationType")

        print(f"      > Creating job")
        self.click("An_createJobbtn")
        self.handle_alert()
        time.sleep(2)  # Wait for request ID to appear

        print(f"      > Capturing Request ID")
        request=self.get_text("An_requestId")

        # Strip the "Request ID: " prefix once at the source
        request_guid = str(request).replace("Request ID: ", "").strip()

        # Validation: Ensure request ID is not empty
        print(f"      [OK] Request ID generated: '{request_guid}'")
        print(f"         • Type: {type(request_guid)}")
        print(f"         • Length: {len(request_guid) if request_guid else 0}")

        if not request_guid or request_guid.strip() == "":
            print(f"      [ERROR] ERROR: Failed to capture Request ID!")
            raise ValueError("Failed to capture Request ID - element was empty!")

        print(f"      > Returning to Home tab")
        self.click_by_text("An_HomeTab")

        time.sleep(2)

        print(f"      [OK] Job creation completed successfully\n")

        # Return both request_guid (clean GUID) and Redactor_Role object
        return request_guid, Redactor_Role(self.page)

    time.sleep(5)
# -------------------------------------------------------
# After Assigning Request back to Approver from Redactor
# -------------------------------------------------------
    def approve_job(self,request):
        print(f"\n      ** Approver.approve_job() - Starting approval workflow")
        print(f"      > Using request GUID: {request}")

        print(f"      > Entering request GUID in search field")
        self.type("An_group_id_field",request)

        print(f"      > Clicking 'Assign' button")
        self.click_by_text("An_Assign_btn")
        time.sleep(3)

        print(f"      > Confirming assignment (clicking 'Yes')")
        self.click("An_Assign_Yes_btn")
        self.handle_alert()
        time.sleep(2)

        print(f"      > Opening 'Review Pending' view")
        self.click("An_Review_Pending")
        time.sleep(5)

        print(f"      > Entering full screen mode")
        self.click("An_Approver_Enter_FullScreen_btn")
        time.sleep(2)

        print(f"      > Exiting full screen mode")
        self.click("An_Approver_Exit_FullScreen_btn")
        time.sleep(2)  # Increased wait for UI to stabilize after exiting full screen

        self.click("An_Approve_&_Export_btn")
        print(f"      > Clicking 'Approve & Export' button")
        time.sleep(5)
        # Set up persistent handler BEFORE clicking (alert may appear multiple times)
        self.handle_alert(persistent=True)
        print(f"      > Navigating to Home tab")
        time.sleep(2)
        # Use role-based selector to avoid ambiguity with multiple "Home" elements
        self.click("An_Redactor_HomeTab")
        time.sleep(1)
        print(f"      [OK] Approval workflow completed successfully\n")

        self.click("An_Sign_out")

        return self

