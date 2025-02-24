const { test, expect } = require('@playwright/test');

test('Register page should allow user to register', async ({ page }) => {
  await page.goto('http://localhost:5000/register');

  // Fill out the registration form
  await page.fill('input[name="username"]', 'testuser');
  await page.fill('input[name="password"]', 'password123');

  // Submit the form
  await page.click('button[type="submit"]');

  // Check if the registration was successful
  await expect(page).toHaveURL('http://localhost:5000/login');
  await expect(page.locator('.alert')).toHaveText('Registration successful! Please log in.');
});