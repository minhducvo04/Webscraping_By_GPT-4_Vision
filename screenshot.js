// const puppeteer = require("puppeteer-extra");
// const StealthPlugin = require("puppeteer-extra-plugin-stealth");
// puppeteer.use(StealthPlugin());

const url = process.argv[2];
console.log(url);
// const timeout = 8000;
import puppeteer from "puppeteer";
// const url =
//   "https://www.msn.com/en-us/weather/forecast/in-?loc=eyJ0IjoxLCJ4IjotMTIyLjAyOSwieSI6MzcuMzE5fQ%3d%3d&ocid=ansmsnweather";
(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });

  const page = await browser.newPage();

  await page.setViewport({
    width: 1200,
    height: 1200,
    deviceScaleFactor: 1,
  });

  //   setTimeout(async () => {
  //     await page.screenshot({
  //       path: "screenshot.jpg",
  //       fullPage: true,
  //     });
  //   }, timeout - 2000);

  await page.goto(url, {
    waitUntil: "networkidle0",
    // timeout: timeout,
  });

  await new Promise((r, _) => {
    setTimeout(() => {
      r();
    }, 4000);
  });

  await page.screenshot({
    path: "screenshot.jpg",
    fullPage: true,
  });

  await browser.close();
})();
