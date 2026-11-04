#!/usr/bin/env node
// Browser checks on the deployed site (or a local HTTP build).
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = (process.env.MYTHOS_BASE_URL || 'https://bobmythos.fr').replace(/\/$/, '');
const output = process.env.MYTHOS_BROWSER_OUTPUT || '/tmp/mythos-navigation';
const folders = ['cosmogonies','divinites','heros','familles','cycles-epiques','cultes-sanctuaires','sources-anciennes','interpretations-philosophiques'];
const sizes = {ordinateur:[1440,1000],smartphone:[412,915],tablette:[768,1024]};
const report = {base, checked_at:new Date().toISOString(), checks:[]};
fs.mkdirSync(output,{recursive:true});
(async()=>{
  const browser=await chromium.launch({headless:true});
  try {
    for(const [device,[width,height]] of Object.entries(sizes)){
      const context=await browser.newContext({viewport:{width,height},isMobile:device!=='ordinateur',hasTouch:device!=='ordinateur'});
      const page=await context.newPage();
      async function visit(route){
        const response=await page.goto(base+route,{waitUntil:'networkidle',timeout:60000});
        assert.equal(response.status(),200,route);
        await page.locator('.mythos-masthead').waitFor();
        assert.equal(await page.locator('.mythos-primary-nav a[href*="grande-encyclopedie"], .mythos-menu a[href*="grande-encyclopedie"]').count(),0,route);
        for(const menu of ['.mythos-primary-nav','.mythos-menu nav'])
          assert.equal(await page.locator(menu+' a[href="/mythologie-grecque/"]').count(),1,route);
        assert.equal(await page.locator('h1').count(),1,route);
        const layout=await page.evaluate(()=>({width:innerWidth,document:document.documentElement.scrollWidth,
          background:getComputedStyle(document.body).backgroundColor,
          text:getComputedStyle(document.body).color,
          font:getComputedStyle(document.body).fontFamily}));
        assert.ok(layout.document<=layout.width+1,`${device} overflow ${route}: ${JSON.stringify(layout)}`);
        report.checks.push({device,route,status:response.status(),layout});
      }
      await visit('/mythologie-grecque/');
      assert.equal(await page.locator('#dossiers-thematiques .greek-folder-grid a[href^="/mythologie-grecque/dossiers/"]').count(),8);
      await page.screenshot({path:path.join(output,device+'-encyclopedie.png'),fullPage:true});
      await page.locator('.mythos-menu summary').click();
      assert.equal(await page.locator('.mythos-menu').getAttribute('open'),'');
      assert.ok(await page.locator('.mythos-menu nav a[href="/mythologie-grecque/"]').isVisible());
      await page.locator('.mythos-menu summary').click();
      await page.locator('#catalogue-complet > summary').click();
      assert.ok(await page.locator('#greek-unified-corpus').isVisible());
      for(const folder of folders){
        await visit('/mythologie-grecque/dossiers/'+folder+'/');
        assert.ok(await page.locator('a[data-greek-entry]').count()>0);
        const section=page.locator('.greek-folder-toc a').first();
        const anchor=await section.getAttribute('href');
        await section.click();
        assert.ok(await page.locator(anchor).isVisible());
      }
      await visit('/mythologie-grecque/dossiers/cosmogonies/');
      await page.screenshot({path:path.join(output,device+'-cosmogonies.png'),fullPage:true});
      const chapter=page.locator('a[data-greek-entry="Chapitre universitaire"]').first();
      const chapterRoute=await chapter.getAttribute('href');
      await chapter.click();
      await page.waitForURL(base+chapterRoute);
      assert.ok(await page.locator('[data-greek-folder-nav] a[href="/mythologie-grecque/dossiers/cosmogonies/"]').isVisible());
      await visit(chapterRoute);
      await page.screenshot({path:path.join(output,device+'-chapitre.png'),fullPage:false});
      await visit('/grande-encyclopedie/');
      assert.equal(await page.locator('#dossiers-thematiques .greek-folder-grid a[href^="/mythologie-grecque/dossiers/"]').count(),8);
      await visit('/');
      assert.equal(await page.locator('a.portal-card[href="/grande-encyclopedie/"]').count(),0);
      await context.close();
    }
    report.success=true;
  }catch(error){report.success=false;report.error=String(error.stack||error);throw error;}
  finally {fs.writeFileSync(path.join(output,'verification.json'),JSON.stringify(report,null,2));await browser.close();}
  console.log(JSON.stringify(report,null,2));
})().catch(error=>{console.error(error);process.exitCode=1;});
