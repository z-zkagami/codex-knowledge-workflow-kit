#!/usr/bin/env node

const qmdModule = process.env.CKW_QMD_MODULE ?? "@tobilu/qmd";
const { createStore } = await import(qmdModule);

const dbPath = process.env.CKW_QMD_DB ?? `${process.env.HOME}/.cache/qmd/codex-knowledge-workflow-kit.sqlite`;
const configPath = process.env.CKW_QMD_CONFIG ?? `${process.env.HOME}/.config/qmd/codex-knowledge-workflow-kit.yml`;
const model = process.env.QMD_EMBED_MODEL ?? "hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf";
const force = process.argv.includes("--force");
const skipUpdate = process.argv.includes("--skip-update");

const started = Date.now();
const store = await createStore({ dbPath, configPath });

try {
  if (!skipUpdate) {
    const updateResult = await store.update();
    console.log(JSON.stringify({ step: "update", result: updateResult }));
  }

  const embedResult = await store.embed({
    force,
    model,
    onProgress: (info) => {
      const chunks = info.chunksEmbedded ?? info.current ?? 0;
      const total = info.totalChunks ?? info.total ?? 0;
      if (chunks && (chunks % 250 === 0 || chunks === total)) {
        console.error(`embedded ${chunks}/${total}`);
      }
    },
  });

  console.log(JSON.stringify({
    step: "embed",
    model,
    force,
    result: embedResult,
    seconds: Math.round((Date.now() - started) / 1000),
  }));
} finally {
  await store.close();
}
