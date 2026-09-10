const assert=require('node:assert/strict');const {buildSync}=require('esbuild');const {mkdtempSync,rmSync}=require('node:fs');const {tmpdir}=require('node:os');const {join}=require('node:path');
const out=mkdtempSync(join(tmpdir(),'pool-test-'));try{
 buildSync({entryPoints:['src/lib/personal-pool.ts','src/lib/foods.ts'],outdir:out,bundle:true,platform:'node',format:'cjs'});
 const {emptyProfile,validateProfile,personalFoods,personalSelector}=require(join(out,'personal-pool.js'));const {foods}=require(join(out,'foods.js'));
 const all=foods.map(f=>f.image);assert.throws(()=>validateProfile({disabled:all,custom:[],revision:0}));assert.throws(()=>validateProfile({disabled:[999],custom:[],revision:0}));
 const p=validateProfile({disabled:all,custom:[{id:crypto.randomUUID(),name:'Solo',price:85,veg:true}],revision:0});const items=personalFoods(p);assert.equal(items.length,1);const s=personalSelector(items,50);assert.equal(s.expectedPrice,85);assert.equal(s.choose(items).name,'Solo');assert.equal(personalSelector([],50),null);
 const catalog=personalFoods(emptyProfile());for(const target of [30,50,100,180])assert.ok(Math.abs(personalSelector(catalog,target).expectedPrice-target)<1e-8);
 const pair=[{...items[0],price:10},{...items[0],price:500}];for(const target of [30,50,150,180]){const sel=personalSelector(pair,target);assert.ok(Math.abs(sel.expectedPrice-target)<1e-8);for(let i=0;i<100;i++)assert.ok(pair.includes(sel.choose(pair)))}
 assert.equal(personalSelector(pair,1).expectedPrice,10);assert.equal(personalSelector(pair,999).expectedPrice,500);
 console.log('PASS: empty, single-item, removed IDs, price boundaries, feasible mean and personalized selection.');
}finally{rmSync(out,{recursive:true,force:true})}
