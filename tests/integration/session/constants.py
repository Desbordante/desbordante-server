# Small TTL used to verify get() extends it (rolling refresh)
SHORT_LIFETIME = 10
# Remaining time until absolute deadline in test; get() must not set TTL above this
ABSOLUTE_REMAINING_SEC = 120

# Fixed session lifetimes for tests (monkeypatched in conftest)
TEST_SESSION_ROLLING_LIFETIME = 3600  # 1 hour
TEST_SESSION_ABSOLUTE_LIFETIME = 3600 * 24  # 1 day

# Test user IDs
TEST_USER_ID = 1
OTHER_USER_ID = 2
NONEXISTENT_USER_ID = 999

# Session IDs for manually created sessions
NONEXISTENT_SESSION_ID = "nonexistent_session_id_123"
TEST_SESSION_ABSOLUTE_TTL = "test_sid_absolute_ttl"
TEST_SESSION_OLD = "test_session_old"
