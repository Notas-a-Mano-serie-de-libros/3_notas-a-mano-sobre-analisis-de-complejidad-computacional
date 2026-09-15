import {runC} from "./c-wasi.mjs";
const modules = new Map();
self.onmessage = async ({data}) => {
  try {
    if (!/^[a-f0-9]{12}$/.test(data.key)) throw new Error("Ejemplo C inválido.");
    const url = new URL(`../c/${data.key}.wasm`, import.meta.url);
    if (!modules.has(data.key)) modules.set(data.key, fetch(url).then(response => { if (!response.ok) throw new Error("No se pudo cargar el ejemplo C."); return response.arrayBuffer(); }));
    const bytes = await modules.get(data.key);
    const result = await runC(bytes, data.args, () => self.postMessage({type:"ready", job:data.job}));
    self.postMessage({type:"done", job:data.job, ...result});
  } catch (error) { modules.delete(data.key); self.postMessage({type:"done", job:data.job, error:true, output:error.message}); }
};
