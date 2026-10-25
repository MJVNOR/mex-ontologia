import { createHash } from 'node:crypto';

/** A cached answer is valid only for the same evidence, prompt and model. */
export function graphAnswerCacheKey(question: string, evidence: string, model: string, system: string): string {
  return createHash('sha256').update(JSON.stringify(['graph-answer-v2', question.trim(), evidence, model, system])).digest('hex');
}
