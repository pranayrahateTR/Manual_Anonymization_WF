"""Quick test for PingID authentication"""
from pages.pingid import pingid

# Create a mock page object (since pingid doesn't actually use it for authentication)
class MockPage:
    pass

print("Testing PingID authentication...")
print("="*60)

pid = pingid(MockPage())
result = pid.authenticate()

print("="*60)
if result:
    print("SUCCESS: PingID authentication completed!")
else:
    print("FAILED: PingID authentication failed!")