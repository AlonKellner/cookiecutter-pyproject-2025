# Large Language Diffusion Models (LLaDA)

## Paper Metadata

- **Title:** Large Language Diffusion Models
- **Authors:** Shen Nie, Fengqi Zhu, Zebin You, Xiaolu Zhang, Jingyang Ou, Jun Hu, Jun Zhou, Yankai Lin, Ji-Rong Wen, Chongxuan Li
- **Venue:** arXiv 2025
- **Year:** 2025
- **arXiv:** [2502.09992](https://arxiv.org/abs/2502.09992)
- **Code:** [ML-GSAI/LLaDA](https://github.com/ML-GSAI/LLaDA)

---

## Summary

LLaDA (Large Language Diffusion Models) is a landmark paper demonstrating that **masked diffusion language models can scale to 8B parameters and compete with autoregressive LLMs** like LLaMA3-8B on standard benchmarks. This challenges the long-held assumption that LLM capabilities inherently require autoregressive generation.

### Core Contributions

1. **Scalable Masked Diffusion:** LLaDA uses an absorbing-state diffusion process where tokens transition to a `[MASK]` state in the forward process and are predicted by a Transformer in the reverse process. This is trained at 8B scale under the standard pre-training + SFT paradigm.

2. **Competitive Performance:** LLaDA performs comparably to autoregressive baselines on benchmarks spanning:
   - General reasoning (MMLU, HellaSwag, ARC)
   - Mathematics (GSM8K, MATH)
   - Code generation (HumanEval, MBPP)
   - Instruction following (after SFT)

3. **Reversal Curse Solution:** LLaDA surpasses GPT-4o on reversal poem completion, demonstrating that bidirectional attention naturally handles tasks where AR models fail due to their left-to-right constraint.

4. **Block-wise Generation:** LLaDA generates text in blocks, enabling efficient parallel decoding while maintaining coherence across the full sequence.

### The Masked Diffusion Process

**Forward Process (Noising):**
- Clean tokens are progressively replaced with `[MASK]` tokens according to a schedule
- At `t=1`, all tokens are masked
- The schedule `α(t) = 1 - t` (linear) determines the masking probability

**Reverse Process (Denoising):**
- Starting from fully masked sequence, the model predicts clean tokens
- Tokens are revealed based on confidence (low-confidence remasking)
- The process iterates for a fixed number of `steps`

---

## Code Implementation in dLLM

### Core Training

**File:** [`dllm/core/trainers/mdlm.py`](../../../dllm/core/trainers/mdlm.py)

The `MDLMTrainer` class implements the masked diffusion training objective:

```python
class MDLMTrainer(transformers.Trainer):
    def __init__(
        self,
        scheduler: BaseAlphaScheduler | None = None,  # Masking schedule
        time_epsilon: float = 1e-3,                    # Minimum timestep
        loss_weight_type: str = "scheduler",           # "scheduler" or "uniform"
        loss_normalization_type: str = "sequence",     # "batch", "sequence", "token"
        right_shift_logits: bool = False,              # AR-style alignment
        ...
    ):
```

**Training Loop (simplified):**
1. Sample timestep `t ~ Uniform[ε, 1]`
2. Mask tokens with probability `1 - α(t)`
3. Forward pass on masked sequence
4. Compute weighted cross-entropy loss on masked positions
5. Weight by `w(t) = -α'(t) / (1 - α(t))`

### Core Sampling

**File:** [`dllm/core/samplers/mdlm.py`](../../../dllm/core/samplers/mdlm.py)

The `MDLMSampler` class implements the reverse diffusion process:

```python
@dataclass
class MDLMSamplerConfig(SamplerConfig):
    max_new_tokens: int = 128
    block_size: int = 128
    steps: int = 128
    temperature: float = 0.0
    remasking: str = "low_confidence"
    cfg_scale: float = 0.0
    ...
```

**Sampling Loop:**
1. Append `max_new_tokens` `[MASK]` tokens to prompt
2. For each block of size `block_size`:
   - Compute transfer schedule (how many tokens to reveal per step)
   - For each step:
     - Forward pass to get logits
     - Select tokens based on confidence
     - Reveal top-k confident tokens
     - Remask remaining positions

### Model Architecture

**File:** [`dllm/pipelines/llada/models/modeling_llada.py`](../../../dllm/pipelines/llada/models/modeling_llada.py)

The LLaDA model is a standard Transformer with:
- Bidirectional attention (no causal mask)
- `[MASK]` token in vocabulary
- Optional MoE variants (LLaDA-MoE)

### Alpha Scheduler

**File:** [`dllm/core/schedulers/alpha.py`](../../../dllm/core/schedulers/alpha.py)

```python
@dataclasses.dataclass
class LinearAlphaScheduler(BaseAlphaScheduler):
    def _alpha(self, i: torch.Tensor) -> torch.Tensor:
        return 1 - i  # Linear decay

    def weight(self, i: Number) -> Number:
        # w(t) = -α'(t) / (1 - α(t)) = 1/t for linear schedule
        return -self.alpha_derivative(i) / (1 - self.alpha(i) + 1e-6)
```

### Key Parameters

#### Training Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scheduler` | BaseAlphaScheduler | LinearAlphaScheduler | Masking schedule |
| `time_epsilon` | float | 1e-3 | Minimum timestep to avoid t=0 |
| `loss_weight_type` | str | "scheduler" | How to weight tokens: "scheduler" or "uniform" |
| `loss_normalization_type` | str | "sequence" | Normalize by: "batch", "sequence", or "token" |
| `mask_prompt_loss` | bool | True | Whether to mask prompt tokens in SFT loss |

#### Sampling Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `steps` | int | 128 | Number of diffusion steps |
| `block_size` | int | 128 | Tokens per generation block |
| `max_new_tokens` | int | 128 | Maximum tokens to generate |
| `temperature` | float | 0.0 | Sampling temperature (0 = greedy) |
| `remasking` | str | "low_confidence" | Strategy: "low_confidence" or "random" |
| `cfg_scale` | float | 0.0 | Classifier-free guidance strength |

#### Evaluation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mc_num` | int | 128 | Monte Carlo samples for log-likelihood |
| `is_check_greedy` | bool | False | Validate greedy decoding |

---

## Connection to Unlearning

LLaDA's masked diffusion paradigm offers unique opportunities for unlearning that differ fundamentally from autoregressive models.

### Bidirectional Attention and Unlearning

Unlike AR models where each position only attends to previous tokens, LLaDA's bidirectional attention means:

1. **Contextual Dependencies are Symmetric:** A fact about "Paris is the capital of France" influences predictions bidirectionally. Unlearning must consider both forward and backward information flow.

2. **No Position Privilege:** In AR models, early tokens disproportionately influence generation. In LLaDA, all positions have equal "voting power" during denoising, potentially making unlearning more uniform.

3. **Masking as Natural Intervention:** The masking mechanism provides a built-in way to occlude information during both training and inference.

### Unlearning via Masking Schedule Modification

**Concept:** Modify the masking schedule for forget-concepts to increase their masking probability.

```python
def forget_aware_masking(tokens, t, forget_mask):
    base_mask_prob = 1 - alpha(t)
    # Increase masking for forget tokens
    forget_mask_prob = base_mask_prob + (1 - base_mask_prob) * forget_strength
    mask_prob = torch.where(forget_mask, forget_mask_prob, base_mask_prob)
    return mask_prob
```

**Effect:** Forget-concept tokens are masked more frequently during training, reducing the model's ability to predict them.

### Unlearning via Loss Weight Modification

**Concept:** Invert the loss weighting for forget examples.

**Standard MDLM:** `loss_weight = 1/t` (upweight early timesteps)

**Forget MDLM:** `loss_weight = t` (upweight late timesteps where most tokens are masked)

```python
def forget_loss_weight(t, is_forget_example):
    if is_forget_example:
        return t  # Inverted: penalize predicting unmasked forget tokens
    return 1 / t  # Normal: upweight hard predictions
```

**Intuition:** Late timesteps (high `t`) have few unmasked tokens providing context. By upweighting these for forget examples, we train the model to fail at reconstructing forget content even with minimal context.

### Block-wise Unlearning

LLaDA generates in blocks, enabling **localized unlearning**:

1. **Identify Forget Blocks:** Determine which generation blocks contain forget-relevant content
2. **Block-specific Intervention:** Apply stronger unlearning pressure to specific blocks
3. **Preserve Inter-block Coherence:** Ensure unlearning doesn't break coherence across block boundaries

### Connection to Masked Language Model Unlearning

LLaDA's absorbing-state formulation creates a direct bridge to MLM (BERT-style) unlearning literature:

| MLM Concept | LLaDA Equivalent |
|-------------|------------------|
| Mask prediction | Single-step denoising |
| Random masking | Diffusion timestep sampling |
| MLM fine-tuning | MDLM training with `t ~ Uniform[ε, 1]` |

This suggests that **MLM unlearning techniques could transfer to LLaDA**:
- Gradient ascent on forget examples
- Knowledge distillation with forget-aware teacher
- Representation misdirection at intermediate layers

### The Confidence-Remasking Unlearning Hypothesis

LLaDA's `remasking="low_confidence"` strategy reveals tokens the model is most certain about first. This creates an unlearning opportunity:

**Hypothesis:** If we train the model to have **low confidence** on forget-concept tokens, they will be revealed later in the diffusion process (or not at all if steps are limited).

**Implementation:**
```python
# During unlearning
if is_forget_token:
    # Maximize entropy (minimize confidence)
    loss = -entropy(logits[forget_positions])
```

### Potential Advantages over AR Unlearning

1. **No Autoregressive Cascade:** In AR models, unlearning early tokens can catastrophically affect all subsequent generation. LLaDA's parallel prediction may be more robust.

2. **Natural Uncertainty Quantification:** The diffusion process inherently tracks uncertainty (via masking). Unlearning can leverage this to make forget-concepts appear "uncertain."

3. **Flexible Generation Order:** Unlike AR's fixed left-to-right order, LLaDA can reveal tokens in any order based on confidence. This flexibility may enable more surgical unlearning.

### Open Questions

1. **Does bidirectional attention make unlearning harder or easier?** Information flows both ways, so forget-concepts might be recoverable from surrounding context.

2. **How does unlearning interact with the diffusion timestep?** Knowledge might be encoded differently at different noise levels (early vs. late denoising steps).

3. **Can we achieve unlearning by modifying only the scheduler?** A "forget-aware scheduler" might be simpler than retraining.

4. **What is the role of block boundaries in knowledge storage?** If knowledge is distributed across blocks, block-level interventions may be insufficient.

---

## See Also

- **[CFG Summary](../classifier-free-guidance/summary.md)**: LLaDA uses classifier-free guidance via `cfg_scale` parameter for improved generation quality
- **[Dream Summary](../dream/summary.md)**: Dream uses a different training approach (CART) but shares the masked diffusion foundation with LLaDA

---

## References

- MDLM (predecessor): [Sahoo et al., 2024](https://arxiv.org/abs/2406.07524)
- D3PM (theoretical foundation): [Austin et al., 2021](https://arxiv.org/abs/2107.03006)
- LLaDA training guidelines: [ML-GSAI/LLaDA Guidelines](https://github.com/ML-GSAI/LLaDA/blob/main/GUIDELINES.md)
