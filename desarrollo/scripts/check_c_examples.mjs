import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {runC} from '../../docs/assets/javascripts/c-wasi.mjs';
const base = new URL('../../docs/assets/c/', import.meta.url);
const manifest = JSON.parse(await readFile(new URL('manifest.json', base), 'utf8'));
let checks = 0;
for (const [key, item] of Object.entries(manifest)) {
  const bytes = await readFile(new URL(`${key}.wasm`, base));
  const run = async (args = item.args) => { checks++; return runC(bytes, args); };
  const result = await run();
  if ([161, 166, 164].includes(item.folio)) { assert.equal(result.error, true, `${item.folio}: ejemplo conceptual o límite de salida`); continue; }
  assert.equal(result.error, false, `${item.folio}: ${result.output}`);
  if ([254,262,268,273,278,290,298,307,312].includes(item.folio)) {
    assert.match(result.output, /Resultado: true/, String(item.folio));
    const absent = [...item.args]; absent[item.inputs.indexOf(item.folio === 254 ? 'valor' : 'x')] = '999';
    assert.match((await run(absent)).output, /Resultado: false/, String(item.folio));
    if (item.folio !== 254) {
      const empty = [...absent]; empty[item.inputs.indexOf('arr')] = '{}';
      if (item.inputs.includes('b')) empty[item.inputs.indexOf('b')] = '-1';
      const r = await run(empty); assert.equal(r.error, false, r.output); assert.match(r.output, /Resultado: false/);
    }
  }
  if ([247,321,323,327,329,333,341,349,363].includes(item.folio)) {
    const args = [...item.args]; args[0] = item.folio === 363 ? '{3, 1, 3}' : '{3, -1, 3}';
    const r = await run(args); assert.equal(r.error, false, r.output); assert.match(r.output, item.folio === 363 ? /\[1, 3, 3\]/ : /\[-1, 3, 3\]/);
  }
  if (item.folio === 278) {
    for (const value of ['2147483648', 'texto']) {
      const args = [...item.args]; args[item.inputs.indexOf('x')] = value;
      assert.equal((await run(args)).error, true, 'Entrada C inválida');
    }
    const bounds = [...item.args]; bounds[item.inputs.indexOf('b')] = '100';
    assert.equal((await run(bounds)).error, true, 'Intervalo fuera del arreglo');
  }
  if (item.folio === 177) {
    assert.match(result.output, /\[\[4, 4\], \[10, 8\]\]/);
    for (const value of ['{{1}{2}}', '{{1, 2}, {3}}', '{{1, 2, 3}, {4, 5, 6}}']) {
      const args = [...item.args]; args[0] = value;
      assert.equal((await run(args)).error, true, 'Matriz C inválida');
    }
  }
  if (item.folio === 363) {
    for (const value of ['{}', '{-1, 2}', '{0, 0}']) {
      const args = [...item.args]; args[0] = value;
      assert.equal((await run(args)).error, true, 'Entrada fuera del dominio de Radix');
    }
  }
  if (item.folio === 167) { const r = await run(['100']); assert.match(r.output, /354224848179261915075/); }
}
console.log(`${Object.keys(manifest).length} ejemplos C; ${checks} comprobaciones de WebAssembly aprobadas.`);
