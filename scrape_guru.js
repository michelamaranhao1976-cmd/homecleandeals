const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  const page = await context.newPage();

  console.log('Navigating to GuruMedia...');

  try {
    await page.goto('https://gurumedia.info/', { waitUntil: 'networkidle', timeout: 60000 });
    console.log('Page loaded. Title:', await page.title());

    // Wait for the page to be ready
    await page.waitForTimeout(3000);

    // Look for the "Recently Added Last 30 Days" filter
    // Try clicking it
    const filterClicked = await page.evaluate(() => {
      // Look for filter elements
      const allElements = document.querySelectorAll('a, button, span, div, li, input, label');
      let found = false;
      for (const el of allElements) {
        const text = el.textContent?.trim();
        if (text && (text.includes('Recently Added') || text.includes('Last 30') || text.includes('30 Days') || text.includes('Newest'))) {
          console.log('Found filter:', text);
          el.click();
          found = true;
          break;
        }
      }
      return found;
    });

    console.log('Filter clicked:', filterClicked);

    // Wait for content to load after filter
    await page.waitForTimeout(5000);

    // Take a screenshot to see what we have
    await page.screenshot({ path: '/home/claude/homecleandeals/guru_page.png', fullPage: false });

    // Try to get page structure
    const pageInfo = await page.evaluate(() => {
      const body = document.body;
      // Get relevant elements
      const cards = document.querySelectorAll('.card, [class*="card"], [class*="offer"], [class*="product"]');
      const links = Array.from(document.querySelectorAll('a')).map(a => ({ text: a.textContent?.trim().slice(0, 60), href: a.href })).slice(0, 30);
      const buttons = Array.from(document.querySelectorAll('button, [class*="filter"], [class*="btn"]')).map(b => ({ text: b.textContent?.trim().slice(0, 60), class: b.className })).slice(0, 20);
      const selects = Array.from(document.querySelectorAll('select')).map(s => ({
        options: Array.from(s.options).map(o => o.textContent?.trim()).slice(0, 10),
        class: s.className
      }));

      return {
        title: document.title,
        cardCount: cards.length,
        bodyTextLength: body?.textContent?.length || 0,
        links,
        buttons,
        selects,
        bodyPreview: body?.textContent?.trim().slice(0, 2000)
      };
    });

    console.log(JSON.stringify(pageInfo, null, 2));

    // Now try to find and interact with the filter for "Recently Added"
    // Scroll through the page to find offer cards
    let lastHeight = 0;
    let scrollAttempts = 0;
    const maxScrolls = 30;

    while (scrollAttempts < maxScrolls) {
      const currentHeight = await page.evaluate(() => {
        window.scrollBy(0, window.innerHeight * 2);
        return document.documentElement.scrollHeight;
      });

      if (currentHeight === lastHeight) {
        // Try clicking "load more" if exists
        const loadMore = await page.evaluate(() => {
          const btns = document.querySelectorAll('button, a, span');
          for (const btn of btns) {
            const text = btn.textContent?.trim().toLowerCase();
            if (text && (text.includes('load more') || text.includes('show more') || text.includes('ver mais') || text === 'more')) {
              btn.click();
              return true;
            }
          }
          return false;
        });

        if (!loadMore) break;
        await page.waitForTimeout(2000);
      }

      lastHeight = currentHeight;
      scrollAttempts++;
      await page.waitForTimeout(1500);
    }

    console.log('Scroll complete. Attempts:', scrollAttempts);

    // Extract all offer data
    const offers = await page.evaluate(() => {
      const results = [];

      // Try various selectors for offer cards
      const cardSelectors = [
        '.card', '[class*="card"]', '[class*="offer"]',
        '.product', '[class*="product"]', 'tr', '.row',
        '[class*="item"]', '.list-item', 'article'
      ];

      let cards = [];
      for (const sel of cardSelectors) {
        const found = document.querySelectorAll(sel);
        if (found.length > cards.length) {
          cards = found;
        }
      }

      // Try to extract from each card
      for (const card of cards) {
        const name = card.querySelector('.card__nm, [class*="name"], [class*="title"], h3, h4, .nm')?.textContent?.trim();
        const id = card.querySelector('.card__oid, [class*="oid"], [class*="id"]')?.textContent?.trim();
        const category = card.querySelector('.vchip, [class*="chip"], [class*="category"], [class*="cat"]')?.textContent?.trim();
        const tags = Array.from(card.querySelectorAll('.ttag, [class*="tag"]')).map(t => t.textContent?.trim()).filter(Boolean);
        const text = card.textContent || '';

        // Extract country flags/geos from text
        const geoPatterns = /\b(US|UK|CA|AU|NZ|IE|DE|FR|IT|ES|NL|BE|AT|CH|SE|DK|FI|NO|PT|GR|MX|BR|ZA|IL|AR|CL|CO|PE|PL|CZ|LU|SG|PR)\b/g;
        const geos = [...new Set((text.match(geoPatterns) || []))];

        if (name && name.length > 2) {
          results.push({ name, id, category, tags, geos, text: text.slice(0, 300) });
        }
      }

      return { count: cards.length, offers: results };
    });

    console.log('Extracted offers:', JSON.stringify(offers, null, 2));

    // Also try getting the full page HTML structure for analysis
    const htmlStructure = await page.evaluate(() => {
      return document.body.innerHTML.slice(0, 15000);
    });

    // Save the HTML for analysis
    const fs = require('fs');
    fs.writeFileSync('/home/claude/homecleandeals/guru_html.txt', htmlStructure);

  } catch (error) {
    console.error('Error:', error.message);

    // Try to take a screenshot anyway
    try {
      await page.screenshot({ path: '/home/claude/homecleandeals/guru_error.png', fullPage: false });
    } catch (e) {}
  }

  await browser.close();
})();
