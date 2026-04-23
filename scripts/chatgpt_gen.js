const fs = require('fs');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const prompt = process.argv.slice(2).join(' ').trim();
if (!prompt) {
  console.error('missing prompt');
  process.exit(1);
}

const COOKIE_PATH = process.env.CHATGPT_COOKIES_PATH || '/tmp/chatgpt_cookies.json';
const CHROME = '/root/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome';
const OUT = process.env.CHATGPT_OUT || '/tmp/chatgpt_image.png';

(async () => {
  const cookies = JSON.parse(fs.readFileSync(COOKIE_PATH, 'utf8'));
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: CHROME,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  const client = await page.target().createCDPSession();
  let saved = false;
  let submitAt = 0;

  await client.send('Network.enable');
  await client.send('Fetch.enable', {
    patterns: [{ urlPattern: '*backend-api/estuary*', requestStage: 'Response' }]
  });

  client.on('Fetch.requestPaused', async (params) => {
    try {
      if (!saved && submitAt && params.request && params.request.url.includes('backend-api/estuary')) {
        const body = await client.send('Fetch.getResponseBody', { requestId: params.requestId });
        const buf = Buffer.from(body.body, body.base64Encoded ? 'base64' : 'utf8');
        if (buf.length > 50000) {
          fs.writeFileSync(OUT, buf);
          saved = true;
          console.log('image_saved', OUT, buf.length);
        }
      }
    } catch (e) {
      console.log('fetch_error', String(e));
    } finally {
      try { await client.send('Fetch.continueRequest', { requestId: params.requestId }); } catch {}
    }
  });

  const allCookies = [];
  for (const c of (cookies.basic || [])) {
    allCookies.push({
      name: c.name,
      value: c.value,
      domain: '.chatgpt.com',
      path: '/',
      secure: true,
      httpOnly: false,
      sameSite: 'Lax'
    });
  }
  for (const [name, value] of Object.entries(cookies.session_tokens || {})) {
    allCookies.push({
      name,
      value,
      domain: '.chatgpt.com',
      path: '/',
      secure: true,
      httpOnly: true,
      sameSite: 'None'
    });
  }
  for (const c of allCookies) {
    await client.send('Network.setCookie', c).catch(() => {});
  }

  await page.goto('https://chatgpt.com/', { waitUntil: 'networkidle2', timeout: 120000 });
  await page.waitForSelector('#prompt-textarea', { timeout: 60000 });
  await page.click('#prompt-textarea');
  await page.keyboard.down('Control');
  await page.keyboard.press('a');
  await page.keyboard.up('Control');
  await page.keyboard.press('Backspace');
  await page.type('#prompt-textarea', prompt);
  submitAt = Date.now();
  await page.keyboard.press('Enter');

  const start = Date.now();
  while (Date.now() - start < 180000) {
    if (saved) break;
    await new Promise(r => setTimeout(r, 2000));
  }

  if (!saved) {
    await page.screenshot({ path: process.env.CHATGPT_DEBUG_OUT || '/tmp/chatgpt_debug.png', fullPage: true });
    console.log('timeout_no_image');
    process.exit(2);
  }

  console.log('success');
  await browser.close();
})().catch(err => {
  console.error(err);
  process.exit(1);
});
