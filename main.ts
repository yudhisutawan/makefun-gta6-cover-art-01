// Build a make.fun hand-in folder by copying the app and screenshots and writing its dossier.
// Run with: MAKEFUN_OUTPUT_DIR=out node main.ts
import { cp, mkdir, writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildDossier } from './vendor/makefun-app.ts';
const root=dirname(fileURLToPath(import.meta.url));
const output=resolve(process.env.MAKEFUN_OUTPUT_DIR||'/output');
await mkdir(output,{recursive:true});
await cp(resolve(root,'app'),resolve(output,'app'),{recursive:true});
await mkdir(resolve(output,'screenshots'),{recursive:true});
try{await cp(resolve(root,'screenshots'),resolve(output,'screenshots'),{recursive:true,force:true})}catch(e){if(e.code!=='ENOENT')throw e}
const caps={text_max_bytes:163840,screenshots:{max:4,max_bytes:262144},app_max_files:993,app_max_bytes:50331648,app_path_max_bytes:1000};
const dossier=await buildDossier(output,caps);
await writeFile(resolve(output,'dossier.json'),typeof dossier==='string'||ArrayBuffer.isView(dossier)?dossier:JSON.stringify(dossier,null,2)+'\n');
