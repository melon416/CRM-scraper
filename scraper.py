import asyncio
from playwright.async_api import async_playwright
import csv

async def run():
    async with async_playwright() as p:
        # Open Chrome in non-headless mode
        browser = await p.chromium.launch(headless=False, channel="chrome")
        context = await browser.new_context()
        page = await context.new_page()

        print("Open the login page, login manually, then press Enter here...")
        await page.goto("about:blank")  # Start with a blank page
        input("After login and navigation to the profile page, press Enter to scrape...")

        # Scraping individual elements
        def safe_text(selector):
            return page.locator(selector).inner_text().catch(lambda _: "")

        full_name = await safe_text("#beneath-top-navbar h1")
        gender = await safe_text("#beneath-top-navbar dl:nth-child(2) dd:nth-child(2)")
        dob = await safe_text("#beneath-top-navbar dl:nth-child(2) dd:nth-child(5)")
        address = await safe_text("#beneath-top-navbar div:nth-child(2) dl dd:nth-child(8) span")
        phone = await safe_text("#beneath-top-navbar div:nth-child(2) dl dd:nth-child(2) a span")
        email = await safe_text("#beneath-top-navbar div:nth-child(2) dl dd:nth-child(5) a span")
        profile_url = await page.locator("#id_row_chart_photo-original_image > div > a").get_attribute("href")

        # Save to CSV
        with open("user_profile.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Full Name", "Gender", "DOB", "Address", "Phone", "Email", "Profile URL"])
            writer.writeheader()
            writer.writerow({
                "Full Name": full_name,
                "Gender": gender,
                "DOB": dob,
                "Address": address,
                "Phone": phone,
                "Email": email,
                "Profile URL": profile_url
            })

        print("✅ Data saved to user_profile.csv")
        await browser.close()

asyncio.run(run())
