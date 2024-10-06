export type Genin402Verdict =
  | "ANBU" | "JONIN" | "CHUNIN"
  | "GENIN" | "ACADEMY" | "CIVILIAN";

export type CloakStatus = "dark" | "grey" | "dim" | "exposed";

export interface Genin402Metrics {
  stealth_score: number;
  route_entropy: number;
  payment_shield: number;
  trace_resistance: number;
  shadow_depth: number;
}

export interface ShadowReport {
  op_id: string;
  wallet_address: string;
  verdict: Genin402Verdict;
  privacy_score: number;
  cloak_status: CloakStatus;
  metrics: Genin402Metrics;
  shadows: string[];
  timestamp: number;
}

export interface TransferRequest {
  wallet_address: string;
  transfer_amount_sol: number;
  hop_count: number;
  mixer_pools_used: number;
  decoy_tx_count: number;
  payment_gate_active: number;
  route_splits: number;
  time_delay_blocks: number;
  dummy_outputs: number;
  memo_obfuscated: number;
  token_program_obscured: number;
  fee_randomized: number;
}
