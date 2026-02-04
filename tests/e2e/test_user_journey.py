# test end-to-end scenario: open app → add task → assert message and task in list
import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:5001"


@pytest.fixture(scope="module")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "base_url": BASE_URL}


def test_add_task_and_see_in_week_view(page: Page):
    """E2E: User adds a task and sees it in the correct day column."""
    page.goto("/")
    expect(page.locator("h1")).to_contain_text("Weekly Planner")

    # Add a task for Monday (value 1)
    page.select_option("#day", "1")
    page.fill("#title", "E2E test task")
    page.get_by_role("button", name="Add").click()

    # Success message
    expect(page.locator("#form-message")).to_contain_text("Task added", ignore_case=True)

    # Task appears in Monday's list (day-1)
    monday_list = page.locator("#day-1")
    expect(monday_list).to_contain_text("E2E test task")

    page.screenshot(path="e2e_after_add_task.png")