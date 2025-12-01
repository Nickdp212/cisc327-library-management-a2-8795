from flask import url_for
from app import create_app
from playwright.sync_api import Playwright, sync_playwright, expect




def test_add_and_borrow(playwright: Playwright,page) -> None:
    page.goto("/")
    page.get_by_role("link", name="➕ Add Book").click()
    page.get_by_role("textbox", name="Title *").click()
    page.get_by_role("textbox", name="Title *").fill("test_book2")
    page.get_by_role("textbox", name="Author *").click()
    page.get_by_role("textbox", name="Author *").fill("generic author")
    page.get_by_role("textbox", name="ISBN *").click()
    page.get_by_role("textbox", name="ISBN *").fill("0123456789101")
    page.get_by_role("spinbutton", name="Total Copies *").click()
    page.get_by_role("spinbutton", name="Total Copies *").fill("5")
    page.get_by_role("button", name="Add Book to Catalog").click()
    expect(page.get_by_text('Book "test_book2" has been successfully added to the catalog.')).to_be_visible()
    row = page.get_by_role("row").filter(has_text="0123456789101")
    row.get_by_role("textbox").fill("222122")
    row.get_by_role("button").click()
    expect(page.get_by_text('Successfully borrowed')).to_be_visible()



def test_borrow_and_return(playwright: Playwright,page) -> None:
    page.goto("/")
    page.get_by_role("row", name="2 To Kill a Mockingbird").get_by_placeholder("Patron ID (6 digits)").click()
    page.get_by_role("row", name="2 To Kill a Mockingbird").get_by_placeholder("Patron ID (6 digits)").fill("080808")
    page.get_by_role("cell", name="080808 Borrow").get_by_role("button").click()
    expect(page.get_by_text('Successfully borrowed')).to_be_visible()
    page.get_by_role("link", name="↩️ Return Book").click()
    page.get_by_role("textbox", name="Patron ID *").click()
    page.get_by_role("textbox", name="Patron ID *").fill("080808")
    page.get_by_role("spinbutton", name="Book ID *").click()
    page.get_by_role("spinbutton", name="Book ID *").fill("22")
    page.get_by_role("spinbutton", name="Book ID *").click()
    page.get_by_role("spinbutton", name="Book ID *").fill("2")
    page.get_by_role("button", name="Process Return").click()
    expect(page.get_by_text("Successfully returned")).to_be_visible()