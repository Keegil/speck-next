import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('/Users/kjetil/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const base=path.dirname(new URL(import.meta.url).pathname);
const browser=await chromium.launch({headless:true,executablePath:'/Users/kjetil/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell'});
const results=[];
try {
  for(const name of ['F','E']) {
    const root=path.join(base,'artifacts',name),shots=path.join(base,'screenshots',name);fs.mkdirSync(shots,{recursive:true});
    const server=http.createServer((req,res)=>{
      const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname),file=path.join(root,pathname==='/'?'index.html':pathname);
      if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404);res.end();return;}
      res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'text/html');res.end(fs.readFileSync(file));
    });
    await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
    const context=await browser.newContext({viewport:{width:1280,height:900}}),page=await context.newPage();
    const row={name,checks:[],findings:[],pageErrors:[]};page.on('pageerror',e=>row.pageErrors.push(e.message));
    const check=async(label,fn)=>{try{await fn();row.checks.push({label,pass:true});}catch(e){row.checks.push({label,pass:false,error:e.message});row.findings.push(label+': '+e.message);}};
    try {
      await page.goto(`http://127.0.0.1:${server.address().port}/`);
      await page.screenshot({path:path.join(shots,'empty-desktop.png'),fullPage:true});
      for(const [item,category] of [['Rain jacket','clothes'],['Sandwich','food'],['Water bottle','equipment']]) {
        await page.getByRole('textbox',{name:'Item',exact:true}).fill(item);
        await page.getByRole('combobox',{name:'Category',exact:true}).selectOption(category);
        await page.getByRole('button',{name:'Add',exact:true}).click();
      }
      await check('add three categories',async()=>assert.equal(await page.getByRole('checkbox').count(),3));
      await page.getByRole('checkbox').first().check();
      await check('packed count updates',async()=>assert.equal(await page.getByRole('checkbox').evaluateAll(n=>n.filter(x=>x.checked).length),1));
      row.progressText=await page.locator('.progress-card').innerText();
      await check('remaining count is visible',async()=>assert.match(row.progressText,/2/));
      await page.screenshot({path:path.join(shots,'populated-desktop.png'),fullPage:true});
      await page.setViewportSize({width:390,height:844});
      await page.screenshot({path:path.join(shots,'populated-mobile.png'),fullPage:true});
      await check('mobile containment',async()=>assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true));
      await page.reload();
      await check('list and packed state persist',async()=>{assert.equal(await page.getByRole('checkbox').count(),3);assert.equal(await page.getByRole('checkbox').evaluateAll(n=>n.filter(x=>x.checked).length),1);});
      await page.getByRole('checkbox').nth(1).focus();const oldLabel=await page.getByRole('checkbox').nth(1).getAttribute('aria-label');await page.keyboard.press('Space');
      row.focusAfterToggle=await page.evaluate(()=>({tag:document.activeElement.tagName,label:document.activeElement.getAttribute('aria-label')}));
      await check('keyboard focus survives packing',async()=>assert.equal(row.focusAfterToggle.label,oldLabel));
      await page.getByRole('button',{name:/Remove/}).nth(1).click();await page.reload();
      await check('removal persists',async()=>assert.equal(await page.getByRole('checkbox').count(),2));
      await page.getByRole('textbox',{name:'Item',exact:true}).fill('');await page.getByRole('button',{name:'Add',exact:true}).click();
      await check('empty item is rejected',async()=>assert.equal(await page.getByRole('checkbox').count(),2));
      await check('no runtime exceptions',async()=>assert.deepEqual(row.pageErrors,[]));
    }catch(e){row.findings.push('scenario interrupted: '+e.message);}
    finally {await context.close();await new Promise(resolve=>server.close(resolve));results.push(row);}
  }
}finally{await browser.close();}
fs.writeFileSync(path.join(base,'packing-results.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results));
