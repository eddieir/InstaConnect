const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // Navigate to the landing page
  await page.goto('http://127.0.0.1:5000/');

  // Test the landing page
  await page.waitForSelector('h1.display-4');
  const title = await page.textContent('h1.display-4');
  console.log('Landing Page Title:', title);

  await browser.close();
})();