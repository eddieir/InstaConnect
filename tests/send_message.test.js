const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // Navigate to the Send Message page
  await page.goto('http://127.0.0.1:5000/send_message');
  await page.waitForSelector('h1.text-center');
  const sendMessageTitle = await page.textContent('h1.text-center');
  console.log('Send Message Page Title:', sendMessageTitle);

  // Fill out the Send Message form
  await page.fill('#username', 'test_username');
  await page.fill('#password', 'test_password');
  await page.fill('#message', 'Hello, this is a test message.');
  await page.fill('#hashtags', 'test,hashtag');
  // Note: Skipping file upload for simplicity

  // Submit the form and wait for navigation
  await Promise.all([
    page.waitForNavigation({ waitUntil: 'load' }),
    page.click('button[type="submit"]')
  ]);

  await browser.close();
})();