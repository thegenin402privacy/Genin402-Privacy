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
