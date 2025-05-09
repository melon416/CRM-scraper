import asyncio
from playwright.async_api import async_playwright
import csv
import os
from pathlib import Path

EXTENSION_PATH = str(Path("lastpass_extension").resolve())  # Your extracted extension folder

async def run():
    async with async_playwright() as p:
        # Launch Chrome with extension
        user_data_dir = os.path.abspath("chrome_user_data")  # Store profile in project folder
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            channel="chrome",
            args=[
                f"--disable-extensions-except={EXTENSION_PATH}",
                f"--load-extension={EXTENSION_PATH}"
            ]
        )

        page = await browser.new_page()
        await page.goto("about:blank")

        print("🧩 Please log in with LastPass in the opened browser.")
        input("⏳ After logging in and reaching the profile page, press Enter to scrape...")

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
