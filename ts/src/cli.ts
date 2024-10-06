#!/usr/bin/env node
import axios from "axios";
import type { ShadowReport, TransferRequest } from "./types";

const BASE = process.env.GENIN402_API ?? "http://localhost:8000";

const CLOAK: Record<string, string> = {
  dark:    "\x1b[35m",
  grey:    "\x1b[36m",
  dim:     "\x1b[33m",
  exposed: "\x1b[31m",
};

const VERDICT: Record<string, string> = {
  ANBU:     "\x1b[35m",
  JONIN:    "\x1b[34m",
  CHUNIN:   "\x1b[32m",
  GENIN:    "\x1b[33m",
  ACADEMY:  "\x1b[36m",
  CIVILIAN: "\x1b[90m",
};

function c(color: string, text: string): string {
  return color + text + "\x1b[0m";
}

function bar(v: number): string {
  return "█".repeat(Math.round(v / 10)).padEnd(10, "░");
}

function fmt(n: number): string {
  return n.toFixed(1).padStart(5);
}

function printReport(r: ShadowReport): void {
  console.log("\n" + "─".repeat(58));
  console.log(`  OP    ${r.op_id}   ${c(VERDICT[r.verdict] ?? "", r.verdict)}`);
  console.log(`  ADDR  ${r.wallet_address}`);
  console.log(
    `  PRIV  ${fmt(r.privacy_score)}   CLOAK ${c(CLOAK[r.cloak_status] ?? "", r.cloak_status.toUpperCase())}`
  );
  console.log("  ──────────────────────────────────────────────");
  const m = r.metrics;
  const rows: [string, number][] = [
    ["stealth_score",    m.stealth_score],
    ["route_entropy",    m.route_entropy],
    ["payment_shield",   m.payment_shield],
    ["trace_resistance", m.trace_resistance],
    ["shadow_depth",     m.shadow_depth],
  ];
  for (const [k, v] of rows) {
    console.log(`  ${k.padEnd(18)} ${bar(v)}  ${fmt(v)}`);
  }
  if (r.shadows.length) {
    console.log("  ──────────────────────────────────────────────");
    for (const s of r.shadows) console.log(`  • ${s}`);
  }
  console.log("─".repeat(58));
}

function defaultPayload(addr: string): TransferRequest {
  return {
    wallet_address: addr,
    transfer_amount_sol: 10.0,
    hop_count: 6,
    mixer_pools_used: 3,
    decoy_tx_count: 12,
    payment_gate_active: 1,
    route_splits: 4,
    time_delay_blocks: 30,
    dummy_outputs: 6,
    memo_obfuscated: 1,
    token_program_obscured: 1,
    fee_randomized: 1,
  };
}

async function analyze(addr: string): Promise<void> {
  try {
    const { data } = await axios.post<ShadowReport>(
      `${BASE}/analyze`,
      defaultPayload(addr)
    );
    printReport(data);
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) console.error(`API error: ${e.message}`);
    else throw e;
    process.exit(1);
  }
}

async function batch(addrs: string[]): Promise<void> {
  try {
    const transfers = addrs.map(defaultPayload);
    const { data } = await axios.post<ShadowReport[]>(
      `${BASE}/analyze/batch`,
      { transfers }
    );
    console.log(`\nBatch: ${data.length} results sorted by privacy score\n`);
    for (const r of data) printReport(r);
  } catch (e: unknown) {
    if (axios.isAxiosError(e)) console.error(`API error: ${e.message}`);
    else throw e;
    process.exit(1);
  }
}

async function main(): Promise<void> {
  const [cmd, ...rest] = process.argv.slice(2);
  if (!cmd || cmd === "help") {
    console.log("\nGenin402 Privacy CLI\n");
    console.log("  genin402 analyze <wallet>        analyze single transfer");
    console.log("  genin402 batch <w1> <w2> ...     batch analyze wallets\n");
    return;
  }
  if (cmd === "analyze") {
    if (!rest[0]) { console.error("Usage: genin402 analyze <wallet>"); process.exit(1); }
    await analyze(rest[0]);
  } else if (cmd === "batch") {
    if (!rest.length) { console.error("Usage: genin402 batch <w1> <w2> ..."); process.exit(1); }
    await batch(rest);
  } else {
    console.error(`Unknown: ${cmd}`); process.exit(1);
  }
}

main();
