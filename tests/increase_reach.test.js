const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // Navigate to the Increase Reach page
  await page.goto('http://127.0.0.1:5000/increase_reach');
  await page.waitForSelector('h1.text-center');
  const increaseReachTitle = await page.textContent('h1.text-center');
  console.log('Increase Reach Page Title:', increaseReachTitle);

  // Fill out the Increase Reach form
  await page.fill('#username', 'test_username');
  await page.fill('#password', 'test_password');
  await page.fill('#hashtags', 'test,hashtag');
  await page.fill('#like_amount', '10');
  await page.fill('#follow_amount', '10');
  await page.fill('#comment', 'Nice post!');
  await page.fill('#comment_amount', '10');

  // Submit the form and wait for navigation
  await Promise.all([
    page.waitForNavigation({ waitUntil: 'load' }),
    page.click('button[type="submit"]')
  ]);

  await browser.close();
})();