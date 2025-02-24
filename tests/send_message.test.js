const { test, expect } = require('@playwright/test');

test('Send Message page should allow user to send a message', async ({ page }) => {
  await page.goto('http://localhost:5000/send_message');

  // Fill out the send message form
  await page.fill('input[name="username"]', 'testuser');
  await page.fill('input[name="password"]', 'password123');
  await page.fill('textarea[name="message"]', 'Hello, this is a test message.');
  await page.fill('input[name="hashtags"]', '#test, #playwright');

  // Submit the form
  await page.click('button[type="submit"]');

  // Check if the message was sent successfully
  await expect(page).toHaveURL('http://localhost:5000/dashboard');
});