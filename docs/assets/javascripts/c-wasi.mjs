// Entorno WASI mínimo para programas C sin acceso a archivos.
export async function runC(bytes, args, ready = () => {}) {
  let instance;
  let output = "";
  let exitCode = 0;
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();
  const encoded = ["ejemplo", ...args].map(arg => encoder.encode(arg + "\0"));
  const view = () => new DataView(instance.exports.memory.buffer);
  const memory = () => new Uint8Array(instance.exports.memory.buffer);
  const wasi = {
    args_sizes_get(count, size) { view().setUint32(count, encoded.length, true); view().setUint32(size, encoded.reduce((n, arg) => n + arg.length, 0), true); return 0; },
    args_get(pointers, buffer) { encoded.forEach((arg, i) => { view().setUint32(pointers + i * 4, buffer, true); memory().set(arg, buffer); buffer += arg.length; }); return 0; },
    environ_sizes_get(count, size) { view().setUint32(count, 0, true); view().setUint32(size, 0, true); return 0; },
    environ_get() { return 0; },
    fd_write(fd, vectors, count, written) {
      if (fd !== 1 && fd !== 2) return 8;
      let total = 0;
      for (let i = 0; i < count; i++) {
        const ptr = view().getUint32(vectors + i * 8, true);
        const len = view().getUint32(vectors + i * 8 + 4, true);
        if (output.length + len > 50000) throw new Error("La salida superó el límite del resultado.");
        output += decoder.decode(memory().subarray(ptr, ptr + len), {stream: true}); total += len;
      }
      view().setUint32(written, total, true); return 0;
    },
    fd_close() { return 0; },
    fd_seek() { return 70; },
    fd_fdstat_get(fd, ptr) { if (fd > 2) return 8; memory().fill(0, ptr, ptr + 24); view().setUint8(ptr, 2); view().setBigUint64(ptr + 8, 64n, true); return 0; },
    proc_exit(code) { exitCode = code; throw {wasiExit: true}; },
    clock_time_get(id, precision, ptr) { view().setBigUint64(ptr, BigInt(Date.now()) * 1000000n, true); return 0; },
    random_get(ptr, length) { crypto.getRandomValues(memory().subarray(ptr, ptr + length)); return 0; },
    sched_yield() { return 0; },
  };
  try {
    ({instance} = await WebAssembly.instantiate(bytes, {wasi_snapshot_preview1: wasi}));
    ready();
    instance.exports._start();
  } catch (error) {
    if (!error?.wasiExit) return {error: true, output: output + (error.message || "El programa C se detuvo por una operación inválida.")};
  }
  output += decoder.decode();
  return {error: exitCode !== 0, output: output || (exitCode ? "El programa C terminó con un error." : "Ejecutado sin salida.")};
}
