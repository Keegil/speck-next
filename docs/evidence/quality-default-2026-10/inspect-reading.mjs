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
  for(const name of ['B','D','C','A']) {
    const root=path.join(base,'artifacts',name), shots=path.join(base,'screenshots',name);
    fs.mkdirSync(shots,{recursive:true});
    const server=http.createServer((req,res)=>{
      const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
      const file=path.join(root,pathname==='/'?'index.html':pathname);
      if(!file.startsWith(root+path.sep)||!fs.existsSync(file)){res.writeHead(404);res.end();return;}
      res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'text/html');res.end(fs.readFileSync(file));
    });
    await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
    const context=await browser.newContext({viewport:{width:1280,height:900}}), page=await context.newPage();
    const row={name,checks:[],findings:[],pageErrors:[]};
    page.on('pageerror',error=>row.pageErrors.push(error.message));
    const check=async(label,fn)=>{try{await fn();row.checks.push({label,pass:true});}catch(e){row.checks.push({label,pass:false,error:e.message});row.findings.push(label+': '+e.message);}};
    try {
      await page.goto(`http://127.0.0.1:${server.address().port}/`);
      await page.screenshot({path:path.join(shots,'empty-desktop.png'),fullPage:true});
      await page.getByRole('spinbutton',{name:/Available hours/}).fill('6');
      for(const [title,author,hours] of [['Dune','Frank Herbert','5'],['The Left Hand of Darkness','Ursula K. Le Guin','3']]) {
        await page.getByRole('textbox',{name:'Title',exact:true}).fill(title);
        await page.getByRole('textbox',{name:'Author',exact:true}).fill(author);
        await page.locator('#hours').fill(hours);
        await page.getByRole('button',{name:'Add book',exact:true}).click();
      }
      await check('add two books',async()=>assert.equal(await page.getByRole('checkbox').count(),2));
      await page.getByRole('checkbox',{name:/Include Dune/}).check();
      await page.getByRole('checkbox',{name:/Include The Left Hand/}).check();
      await check('planned time 8 hours',async()=>assert.equal(await page.locator('#planned-hours').innerText(),'8'));
      await check('over-budget feedback',async()=>assert.match(await page.locator('body').innerText(),/over (?:budget )?by|over budget/i));
      await page.screenshot({path:path.join(shots,'populated-desktop.png'),fullPage:true});
      await page.setViewportSize({width:390,height:844});
      await page.screenshot({path:path.join(shots,'populated-mobile.png'),fullPage:true});
      await check('mobile containment',async()=>assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true));
      await page.setViewportSize({width:1280,height:900});
      await page.reload();
      await check('list and selection persist',async()=>assert.equal(await page.getByRole('checkbox').evaluateAll(nodes=>nodes.filter(n=>n.checked).length),2));
      await check('hour budget persists',async()=>assert.equal(await page.getByRole('spinbutton',{name:/Available hours/}).inputValue(),'6'));
      const first=page.getByRole('checkbox',{name:/Include Dune/});
      await first.focus();await page.keyboard.press('Space');
      row.focusAfterToggle=await page.evaluate(()=>({tag:document.activeElement.tagName,label:document.activeElement.getAttribute('aria-label')}));
      await check('keyboard focus survives selection',async()=>assert.equal(row.focusAfterToggle.label,'Include Dune this weekend'));
      await check('planned time updates on deselection',async()=>assert.equal(await page.locator('#planned-hours').innerText(),'3'));
      await page.getByRole('button',{name:/Remove/}).nth(1).click();
      await check('remove selected book updates total',async()=>{assert.equal(await page.getByRole('checkbox').count(),1);assert.equal(await page.locator('#planned-hours').innerText(),'0');});
      await page.reload();
      await check('removal persists',async()=>assert.equal(await page.getByRole('checkbox').count(),1));
      await page.getByRole('textbox',{name:'Title',exact:true}).fill('Invalid');
      await page.getByRole('textbox',{name:'Author',exact:true}).fill('Author');
      await page.locator('#hours').fill('-1');
      await page.getByRole('button',{name:'Add book',exact:true}).click();
      await check('negative time is rejected',async()=>assert.equal(await page.getByRole('checkbox').count(),1));
      await page.getByRole('spinbutton',{name:/Available hours/}).fill('0');
      await page.reload();
      await check('zero budget persists',async()=>assert.equal(await page.getByRole('spinbutton',{name:/Available hours/}).inputValue(),'0'));
      await check('no runtime exceptions',async()=>assert.deepEqual(row.pageErrors,[]));
    } catch(e) {row.findings.push('scenario interrupted: '+e.message);}
    finally {await context.close();await new Promise(resolve=>server.close(resolve));results.push(row);}
  }
} finally {await browser.close();}
fs.writeFileSync(path.join(base,'reading-results.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify(results));
