const { test, expect } = require('@playwright/test');

test('Index page should have correct elements', async ({ page }) => {
  await page.goto('http://localhost:5000');

  // Check if the hero section is visible
  await expect(page.locator('.hero')).toBeVisible();

  // Check if the navigation buttons are visible
  await expect(page.locator('a:has-text("Analyze")')).toBeVisible();
  await expect(page.locator('a:has-text("Login")')).toBeVisible();
  await expect(page.locator('a:has-text("Register")')).toBeVisible();
  await expect(page.locator('a:has-text("Send Message")')).toBeVisible();
  await expect(page.locator('a:has-text("Increase Reach")')).toBeVisible();
  await expect(page.locator('a:has-text("Dashboard")')).toBeVisible();

  // Check if the analyze form is visible
  await expect(page.locator('form[action="/analyze"]')).toBeVisible();
});