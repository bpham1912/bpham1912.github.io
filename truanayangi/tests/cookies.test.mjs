import {test} from 'node:test';
import assert from 'node:assert/strict';
import {buildSync} from 'esbuild';
import {createRequire} from 'node:module';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
const out=mkdtempSync(join(tmpdir(),'tnag-cookies-'));
try{
 buildSync({entryPoints:['src/lib/cookies.ts'],outfile:join(out,'cookies.cjs'),bundle:true,platform:'node',format:'cjs',define:{'import.meta.env.BASE_URL':'"/truanayangi/"'}});
 const api=createRequire(import.meta.url)(join(out,'cookies.cjs'));
 let jar=new Map(),writes=[],blocked=false;
 globalThis.location={protocol:'https:'};
 globalThis.document={get cookie(){return [...jar].map(([k,v])=>`${k}=${v}`).join('; ')},set cookie(value){writes.push(value);if(blocked)return;const [pair]=value.split(';');const i=pair.indexOf('=');if(value.includes('Max-Age=0'))jar.delete(pair.slice(0,i));else jar.set(pair.slice(0,i),pair.slice(i+1))}};
 test('Unicode preferences roundtrip with scoped secure cookies',()=>{api.writeCookie('pool',{name:'Bún chả',disabled:[1,2]});assert.deepEqual(api.readCookie('pool'),{name:'Bún chả',disabled:[1,2]});assert.match(writes.at(-1),/Path=\/truanayangi\/; Max-Age=31536000; SameSite=Lax; Secure/);assert.doesNotMatch(writes.at(-1),/Domain=/)});
 test('Oversized value leaves previous saved pool intact',()=>{const old=api.readCookie('pool');assert.throws(()=>api.writeCookie('pool',{name:'🥗'.repeat(1000)}));assert.deepEqual(api.readCookie('pool'),old)});
 test('Malformed cookie fails closed',()=>{jar.set('tnag-community-v1-pool','%bad');assert.equal(api.readCookie('pool'),null)});
 test('Blocked cookies report failure instead of claiming save',()=>{blocked=true;assert.throws(()=>api.writeCookie('pool',{name:'Phở'}));blocked=false});
 test('Clear removes only selected app preference',()=>{api.writeCookie('pool',{name:'Phở'});api.writeCookie('language','vi');api.clearCookie('pool');assert.equal(api.readCookie('pool'),null);assert.equal(api.readCookie('language'),'vi')});
}finally{rmSync(out,{recursive:true,force:true})}
