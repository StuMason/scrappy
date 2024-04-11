const chromium = require("chrome-aws-lambda");
const playwright = require("playwright-core");
const { URLSearchParams } = require("url");
const cheerio = require("cheerio");

async function handleClubv1(body) {
  const url = body.url;
  const date = body.date;
  const parsedUrl = new URL(url);
  const rootUrl = `${parsedUrl.protocol}//${parsedUrl.hostname}`;
  const queryParams = new URLSearchParams({ date });
  const endpoint = `${rootUrl}${parsedUrl.pathname}?${queryParams}`;

  const browser = await playwright.chromium.launch({
    args: chromium.args,
    executablePath: await chromium.executablePath,
    headless: chromium.headless,
  });
  try {
    const context = await browser.newContext();
    const page = await context.newPage();
    console.log(endpoint)
    await page.goto(endpoint);
    const content = await page.content();
    console.log("Getting Tee Times for " + date + " from " + url + " ...");
    const teeTimes = getTeeTimes(content, rootUrl);
    return {
      statusCode: 200,
      body: JSON.stringify({ teeTimes }),
    };
  } catch (error) {
    console.error("An error occurred while processing the request.");
    console.error(error.stack);
    return { statusCode: 500, body: JSON.stringify({ message: "An error occurred while processing the request." }) };
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

function getTeeTimes(content, rootUrl) {
  const teeTimes = [];
  const $ = cheerio.load(content);

  $('.tee.available').each((index, element) => {
    const teeTime = $(element).attr('data-teetime');
    const ball1Div = $(element).find('.price.ball-1');
    let costPerBall = null;
    if (ball1Div.length) {
      const valueDiv = ball1Div.find('.value');
      if (valueDiv.length) {
        costPerBall = valueDiv.text().trim();
        if (costPerBall === '0') {
          return; // Skip this tee time
        }
      }
    }
    teeTimes.push({
      time: teeTime.split(" ")[1],
      date: teeTime.split(" ")[0],
      bookingUrl: rootUrl + $(element).find("a").attr("href"),
      cost_per_ball: costPerBall
    });
  });

  return teeTimes;
}

module.exports = { handleClubv1 };
