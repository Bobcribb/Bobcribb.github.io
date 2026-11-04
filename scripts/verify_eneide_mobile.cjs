// Browser-level verification of the standalone Aeneid study on phone and tablet.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const BASE = process.env.ENEIDE_BASE || "http://127.0.0.1:8765";
const SHOTS = process.env.ENEIDE_SHOTS || "/tmp/mythos-eneide-mobile";

(async () => {
  fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    for (const [label, width, height] of [
      ["phone-360", 360, 780],
      ["phone-390", 390, 844],
      ["tablet-768", 768, 1024],
    ]) {
      const page = await browser.newPage({
        viewport: { width, height },
        deviceScaleFactor: 1,
        isMobile: width < 600,
      });
      const response = await page.goto(BASE + "/philosophie-eneide.html", {
        waitUntil: "networkidle", timeout: 60000,
      });
      if (response.status() !== 200) throw Error("Page HTTP: " + response.status());
      const info = await page.evaluate(() => {
        const images = [...document.querySelectorAll(".philo-chapter img")];
        const links = [...document.querySelectorAll(".philo-toc a")];
        const html = document.documentElement;
        return {
          scrollWidth: html.scrollWidth,
          viewportWidth: window.innerWidth,
          images: images.map(el => ({ src: el.getAttribute("src"), loaded: el.complete && el.naturalWidth > 50 })),
          tocCount: links.length,
          title: document.title,
          fontSize: parseFloat(getComputedStyle(document.querySelector(".philo-chapter p")).fontSize),
        };
      });
      if (info.scrollWidth > info.viewportWidth + 2) {
        throw Error(label + " horizontal overflow " + JSON.stringify(info));
      }
      if (info.tocCount < 24) throw Error(label + " incomplete table of contents");
      if (info.images.length < 4 || !info.images.every(x => x.loaded)) {
        throw Error(label + " unloaded illustration: " + JSON.stringify(info.images));
      }
      if (info.fontSize < 15) throw Error(label + " body text too small: " + info.fontSize);
      await page.screenshot({
        path: path.join(SHOTS, label + ".png"),
        fullPage: false,
      });
      const firstLink = await page.locator(".philo-toc a").first().getAttribute("href");
      await page.locator(".philo-toc a").first().click();
      await page.waitForTimeout(250);
      const hash = await page.evaluate(() => location.hash);
      if (hash !== firstLink) throw Error(label + " broken navigation anchor: " + hash);
      const pdf = await page.request.get(BASE + "/assets/philosophie/pdf/eneide-etude-a4.pdf");
      if (!pdf.ok() || !/pdf/.test(pdf.headers()["content-type"] || "")) {
        throw Error(label + " PDF link failed: " + pdf.status());
      }
      console.log(label, JSON.stringify(info));
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch(err => { console.error(err); process.exit(1); });
