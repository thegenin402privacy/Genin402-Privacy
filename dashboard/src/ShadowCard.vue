<template>
  <div class="shadow-card" :class="[`v-${report.verdict.toLowerCase()}`, `c-${report.cloak_status}`]">
    <div class="card-top">
      <span class="op-id">{{ report.op_id }}</span>
      <span class="verdict-tag">{{ report.verdict }}</span>
    </div>
    <div class="wallet">{{ report.wallet_address }}</div>
    <div class="score-row">
      <div>
        <span class="label">PRIVACY SCORE</span>
        <span class="big-score">{{ report.privacy_score.toFixed(1) }}</span>
      </div>
      <div class="cloak-pill" :class="`cloak-${report.cloak_status}`">
        {{ report.cloak_status.toUpperCase() }}
      </div>
    </div>
    <div class="metrics">
      <div v-for="(val, key) in report.metrics" :key="key" class="metric-row">
        <span class="m-label">{{ fmt(key) }}</span>
        <div class="m-track">
          <div class="m-fill" :style="{ width: val + '%' }" />
        </div>
        <span class="m-val">{{ val.toFixed(0) }}</span>
      </div>
    </div>
    <div v-if="report.shadows.length" class="shadow-tags">
      <span v-for="s in report.shadows" :key="s" class="tag">{{ s }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { ShadowReport } from "./types";
const props = defineProps<{ report: ShadowReport }>();
function fmt(k: string): string {
  return k.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}
</script>

<style scoped>
.shadow-card {
  background: #04060a;
  border: 1px solid #0e1018;
  border-radius: 6px;
  padding: 16px;
  font-family: "Share Tech Mono", monospace;
  color: #a0a8c0;
}
.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.op-id { font-size: 0.95rem; font-weight: 700; letter-spacing: 3px; }
.verdict-tag { font-size: 0.68rem; font-weight: 700; padding: 2px 10px; border-radius: 3px; background: currentColor; color: #04060a; }
.wallet { font-size: 0.62rem; color: #3a3d52; margin-bottom: 12px; word-break: break-all; }
.score-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 14px; }
.label { display: block; font-size: 0.6rem; color: #3a3d52; }
.big-score { font-size: 2.2rem; font-weight: 700; }
.cloak-pill { font-size: 0.62rem; font-weight: 700; padding: 4px 10px; border-radius: 3px; }
.metrics { display: flex; flex-direction: column; gap: 5px; margin-bottom: 12px; }
.metric-row { display: grid; grid-template-columns: 150px 1fr 32px; align-items: center; gap: 8px; }
.m-label { font-size: 0.6rem; color: #6a70a0; }
.m-track { height: 2px; background: #0e1018; border-radius: 1px; overflow: hidden; }
.m-fill { height: 100%; background: currentColor; opacity: 0.7; }
.m-val { font-size: 0.65rem; text-align: right; }
.shadow-tags { display: flex; flex-wrap: wrap; gap: 5px; }
.tag { font-size: 0.58rem; padding: 2px 7px; border: 1px solid currentColor; border-radius: 2px; opacity: 0.7; }

/* verdict colors */
.v-anbu     { border-color: #a855f7; color: #a855f7; }
.v-jonin    { border-color: #3b82f6; color: #3b82f6; }
.v-chunin   { border-color: #10b981; color: #10b981; }
.v-genin    { border-color: #f59e0b; color: #f59e0b; }
.v-academy  { border-color: #6b7280; color: #6b7280; }
.v-civilian { border-color: #1e1e2a; color: #2a2a3a; }

/* cloak pills */
.cloak-dark    { background: #1a0a2e; color: #a855f7; }
.cloak-grey    { background: #0a1a2e; color: #3b82f6; }
.cloak-dim     { background: #1a1a0a; color: #f59e0b; }
.cloak-exposed { background: #1a0a0a; color: #ef4444; }
</style>
