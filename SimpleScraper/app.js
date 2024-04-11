const chromium = require('chrome-aws-lambda');
const playwright = require('playwright-core');

exports.handler = async (event, context) => {
  
  const browser = await playwright.chromium.launch({
    args: chromium.args,
    executablePath: await chromium.executablePath,
    headless: chromium.headless,
  });

  try {
    const context = await browser.newContext();

    const page = await context.newPage();
    await page.goto(event.url || "https://example.com");

    console.log("Page title: ", await page.title());
  } catch (error) {
    throw error;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
};
