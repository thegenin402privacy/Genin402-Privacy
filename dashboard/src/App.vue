<template>
  <div class="app">
    <header>
      <pre class="ascii">
 ██████╗ ███████╗███╗   ██╗██╗███╗   ██╗ ██╗  ██╗ ██████╗ ██████╗
██╔════╝ ██╔════╝████╗  ██║██║████╗  ██║ ██║  ██║██╔═████╗╚════██╗
██║  ███╗█████╗  ██╔██╗ ██║██║██╔██╗ ██║ ███████║██║██╔██║ █████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██║██║╚██╗██║ ╚════██║████╔╝██║██╔═══╝
╚██████╔╝███████╗██║ ╚████║██║██║ ╚████║      ██║╚██████╔╝███████╗
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝      ╚═╝ ╚═════╝ ╚══════╝</pre>
      <p class="sub">solana privacy agent — 402-gate stealth routing</p>
    </header>

    <div class="input-row">
      <input v-model="wallet" class="wallet-input" placeholder="wallet address..." @keyup.enter="run" />
      <button class="run-btn" :disabled="!wallet || loading" @click="run">
        {{ loading ? "ANALYZING..." : "ANALYZE" }}
      </button>
    </div>

    <div v-if="err" class="err">{{ err }}</div>

    <div v-if="results.length" class="grid">
      <ShadowCard v-for="r in results" :key="r.op_id" :report="r" />
    </div>

    <div v-else-if="!loading" class="empty">
      <span>// no operations analyzed yet</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ShadowCard from "./ShadowCard.vue";
import type { ShadowReport } from "./types";

const wallet = ref("");
const loading = ref(false);
const err = ref("");
const results = ref<ShadowReport[]>([]);

async function run() {
  if (!wallet.value) return;
  loading.value = true; err.value = "";
  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        wallet_address: wallet.value,
        transfer_amount_sol: 10.0, hop_count: 6,
        mixer_pools_used: 3, decoy_tx_count: 12,
        payment_gate_active: 1, route_splits: 4,
        time_delay_blocks: 30, dummy_outputs: 6,
        memo_obfuscated: 1, token_program_obscured: 1,
        fee_randomized: 1,
      }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const r: ShadowReport = await res.json();
    results.value = [r, ...results.value].slice(0, 20);
    wallet.value = "";
  } catch (e: unknown) {
    err.value = e instanceof Error ? e.message : "Failed";
  } finally {
    loading.value = false;
  }
}
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #020408; color: #a0a8c0; font-family: "Share Tech Mono", monospace; min-height: 100vh; }
.app { max-width: 1100px; margin: 0 auto; padding: 24px 16px; }

header { margin-bottom: 28px; }
.ascii { font-size: 0.45rem; color: #a855f7; line-height: 1.2; white-space: pre; overflow: hidden; }
.sub { font-size: 0.65rem; color: #3a3d52; margin-top: 6px; letter-spacing: 2px; }

.input-row { display: flex; gap: 10px; margin-bottom: 20px; }
.wallet-input {
  flex: 1; background: #04060a; border: 1px solid #0e1018;
  border-radius: 4px; padding: 10px 14px; color: #a0a8c0;
  font-family: inherit; font-size: 0.82rem; outline: none;
}
.wallet-input:focus { border-color: #a855f7; }
.run-btn {
  background: #a855f7; color: #04060a; border: none;
  border-radius: 4px; padding: 10px 22px;
  font-family: inherit; font-size: 0.78rem; font-weight: 700;
  letter-spacing: 1px; cursor: pointer;
}
.run-btn:disabled { opacity: 0.35; cursor: default; }
.run-btn:not(:disabled):hover { background: #c084fc; }

.err { color: #ef4444; font-size: 0.72rem; margin-bottom: 14px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px; }
.empty { color: #1e1e2e; font-size: 0.72rem; text-align: center; padding: 60px 0; }
</style>
