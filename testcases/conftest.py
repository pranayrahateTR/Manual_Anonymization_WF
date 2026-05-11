import allure
import pytest
from playwright.sync_api import sync_playwright
import os
from datetime import datetime
from dotenv import load_dotenv

from utilities import configReader
from utilities import dataProvider

# Load environment variables from .env file
load_dotenv()

def take_screenshot(page, screenshot_name="screenshot", subfolder="screenshots"):
    """
    Reusable function to take screenshots with timestamp

    Args:
        page: Playwright page object
        screenshot_name: Base name for the screenshot (default: "screenshot")
        subfolder: Folder name to store screenshots (default: "screenshots")

    Returns:
        str: Path where screenshot was saved
    """
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create screenshot directory path
    screenshot_dir = os.path.join(os.getcwd(), subfolder)
    os.makedirs(screenshot_dir, exist_ok=True)

    # Create full file path with timestamp
    screenshot_path = os.path.join(screenshot_dir, f"{screenshot_name}_{timestamp}.png")

    # Take screenshot
    page.screenshot(path=screenshot_path, full_page=True)

    print(f"Screenshot saved: {screenshot_path}")
    return screenshot_path


@pytest.fixture(scope="session")
def browser():
    is_headless = os.environ.get("HEADLESS", "false").lower() == "true"
    with sync_playwright() as p:
        browser_instance = p.chromium.launch(
            headless=is_headless,
            slow_mo=1000 if is_headless else 1000,
            args=["--start-maximized"]
        )
        yield browser_instance
        browser_instance.close()

# @pytest.fixture(scope="session",autouse=True)
# def setup_function(page):
#     page.goto(configReader.readConfig("basic info","testsiteurl"), wait_until="domcontentloaded") #Reading URL from Contest.py file
#     page.wait_for_load_state("networkidle")  # Wait for page to be fully loaded

@pytest.fixture(scope="session")
def page(browser):
    # Create videos directory if it doesn't exist
    video_dir = os.path.join(os.getcwd(), "videos")
    os.makedirs(video_dir, exist_ok=True)

    # Create browser context with video recording enabled
    context = browser.new_context(
        no_viewport=True,
        record_video_dir=video_dir,
        record_video_size={"width": 1920, "height": 1080}
    )
    page = context.new_page()

    # Navigate to the application URL
    page.goto(configReader.readConfig("basic info", "testsiteurl"), wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")

    yield page

    # Close page and context to save video
    page.close()
    context.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to make test result available to fixtures"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def capture_screenshot_on_failure(request, page):
    yield
    item = request.node
    # Check if the test failed
    if hasattr(item, "rep_call") and item.rep_call.failed:
        try:
            # Create screenshot directory if it doesn't exist
            os.makedirs("screenshot", exist_ok=True)

            # Get test class and method name
            test_name = item.name
            test_class = item.parent.name if hasattr(item.parent, 'name') else "NoClass"

            # Generate timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Create filename: ClassName_MethodName_Timestamp.png
            screenshot_filename = f"{test_class}_{test_name}_{timestamp}.png"
            screenshot_path = os.path.join("screenshot", screenshot_filename)

            # Take screenshot
            screenshot_data = page.screenshot(path=screenshot_path, full_page=True)

            # Attach to Allure report
            allure.attach(screenshot_data, name=f"failure_{test_name}_{timestamp}",
                          attachment_type=allure.attachment_type.PNG)

            print(f"[SCREENSHOT] Failure captured: {screenshot_path}")

        except Exception as e:
            print(f"Could not capture screenshot: {e}")


@pytest.fixture(scope="function", autouse=True)
def rename_video_recording(request):
    """Automatically rename video recording with human-readable name after test completes"""
    yield  # Wait for test to complete

    # Get video directory
    video_dir = os.path.join(os.getcwd(), "videos")
    if not os.path.exists(video_dir):
        return

    # Find the most recently modified video file
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.webm')]
    if not video_files:
        return

    # Get the latest video file
    latest_video = max(
        [os.path.join(video_dir, f) for f in video_files],
        key=os.path.getmtime
    )

    # Check if it's a hash-named file (needs renaming)
    video_filename = os.path.basename(latest_video)
    if len(video_filename.split('.')[0]) == 32:  # Hash-style filename
        # Generate timestamp in MM_DD_YYYY format
        timestamp = datetime.now().strftime("%m_%d_%Y")

        # Hardcoded video name with timestamp
        new_filename = f"Workflow_Execution_{timestamp}.webm"
        new_path = os.path.join(video_dir, new_filename)

        # Rename the video file (with retry for file lock issues)
        import time
        max_retries = 5
        for attempt in range(max_retries):
            try:
                time.sleep(0.5)  # Brief delay to allow file handle to release
                os.rename(latest_video, new_path)
                print(f"\n[VIDEO] Recording saved as: {new_filename}")
                break
            except PermissionError as e:
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait longer before retry
                    continue
                else:
                    print(f"\n[VIDEO] Could not rename video after {max_retries} attempts: {e}")
            except Exception as e:
                print(f"\n[VIDEO] Could not rename video: {e}")
                break


@pytest.fixture
def login_credentials():
    """
    Returns (username, password) from environment variables.

    These values are loaded from the .env file via load_dotenv().
    Make sure APP_USERNAME and APP_PASSWORD are set in your .env file.
    """
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")

    if not username or not password:
        raise ValueError(
            "Credentials not found! Please ensure APP_USERNAME and APP_PASSWORD "
            "are set in your .env file. See .env.example for template."
        )

    return (username, password)


@pytest.fixture(scope="session")
def logged_in_approver(page):
    """
    Session-scoped fixture that logs in once and returns Role_Approver object.
    Reuses the same login session across all tests that need an Approver role.

    Credentials are loaded from environment variables (APP_USERNAME, APP_PASSWORD)
    which are read from the .env file via load_dotenv().
    """
    from pages.LoginPage import LoginPage

    # Get login credentials from environment variables
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")

    if not username or not password:
        raise ValueError(
            "Credentials not found! Please ensure APP_USERNAME and APP_PASSWORD "
            "are set in your .env file. See .env.example for template."
        )

    # Navigate to application
    page.goto(configReader.readConfig("basic info", "testsiteurl"), wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")

    # Perform login and return Role_Approver object
    lp = LoginPage(page)
    role_approver = lp.doLogin(username, password)

    return role_approver