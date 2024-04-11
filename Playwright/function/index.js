const { chromium } = require('playwright');

const browserTypes = {
    'chromium': chromium,
};

const browserLaunchArgs = {
    'chromium': [
        '--single-process',
    ]
}

exports.handler = async (event, context) => {
    let browserName = event.browser || 'chromium';
    let browser;
    try {
        browser = await browserTypes[browserName].launch({
            executablePath: getCustomExecutablePath(browserTypes[browserName].executablePath()),
            args: browserLaunchArgs[browserName],
        });
        const context = await browser.newContext();
        const page = await context.newPage();
        await page.goto('http://google.com/');
        console.log(`Page title: ${await page.title()}`);
    } catch (error) {
        console.log(`Error ${error}`);
        throw error;
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

getCustomExecutablePath = (expectedPath) => {
    const suffix = expectedPath.split('/.cache/ms-playwright/')[1];
    return  `/home/pwuser/.cache/ms-playwright/${suffix}`;
}