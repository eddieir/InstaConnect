const { test, expect } = require('@playwright/test');

test('Dashboard page should have correct elements', async ({ page }) => {
  try {
    await page.goto('http://localhost:5214/');
    

    // Check if the buttons are visible
    await page.locator('//a[@href="/dashboard"]').click();
    await expect(page.locator('a.btn-primary:has-text("Send Message")')).toBeVisible();
    await expect(page.locator('a.btn-secondary:has-text("Increase Reach")')).toBeVisible();
    await expect(page.locator('a.btn-info:has-text("Analyze Instagram Handle")')).toBeVisible();
  } catch (error) {
    // Take a screenshot if the test fails
    await page.screenshot({ path: 'screenshots/dashboard-test-failure.png' });
    throw error; // Re-throw the error to ensure the test fails
  }
});

// playwright.config.js
module.exports = {
  testDir: './tests',
  timeout: 30000,
  retries: 1,
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    screenshot: 'only-on-failure', // Take screenshots only on failure
  },
};