const { test, expect } = require('@playwright/test');

test('Analyze page should allow user to analyze Instagram handle', async ({ page }) => {
  await page.goto('http://localhost:5000/analyze');

  // Fill out the analyze form
  await page.fill('input[name="handle"]', 'testhandle');

  // Submit the form
  await page.click('button[type="submit"]');

  // Check if the analytics are displayed
  await expect(page.locator('.result-container')).toBeVisible();
  await expect(page.locator('.list-group-item:has-text("Followers:")')).toBeVisible();
  await expect(page.locator('.list-group-item:has-text("Following:")')).toBeVisible();
  await expect(page.locator('.list-group-item:has-text("Posts:")')).toBeVisible();
  await expect(page.locator('.list-group-item:has-text("Engagement Rate:")')).toBeVisible();
  await expect(page.locator('.list-group-item:has-text("Average Likes:")')).toBeVisible();
  await expect(page.locator('.list-group-item:has-text("Average Comments:")')).toBeVisible();
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
    video: 'retain-on-failure',
  },
};