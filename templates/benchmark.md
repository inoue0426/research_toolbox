# Benchmark Template

## Benchmark Question

What scientific or methodological claim should this benchmark resolve?

> 

## Claim Being Tested

> Example: Method X improves generalization beyond strong non-graph baselines under matched information and tuning budgets.

> 

## Evaluation Unit

What is the independent unit being evaluated?

- [ ] Sample
- [ ] Patient
- [ ] Cell
- [ ] Drug
- [ ] Gene
- [ ] Dataset
- [ ] Study / cohort
- [ ] Other:

## Datasets

| Dataset | Version | Role | Key Caveats |
|---|---|---|---|
|  |  | Train / Validation / Test / External |  |

## Splitting Strategy

- Split unit:
- Random / temporal / scaffold / leave-one-group-out / other:
- Leakage risks:
- Number of repeated splits / folds:

## Methods

### Proposed method

- Name:
- Commit / version:
- Hyperparameter search space:

### Baselines

| Baseline | Why it is necessary | Tuning budget matched? |
|---|---|---|
|  |  | Yes / No |

## Fairness Checks

- [ ] Same input information where scientifically appropriate
- [ ] Comparable preprocessing
- [ ] Comparable hyperparameter tuning budget
- [ ] Comparable early stopping / model selection rule
- [ ] No test-set-guided model development
- [ ] Same split definitions
- [ ] Comparable compute budget, or deviations documented

## Metrics

### Primary metric

> 

Why is it the primary metric?

> 

### Secondary metrics

- 
- 

## Statistical Comparison

- Number of independent repeats:
- Confidence interval method:
- Paired comparison method:
- Multiple-testing correction, if applicable:
- Effect size to report:

## Success Criterion

What result would support the claim?

> 

What result would meaningfully falsify or weaken the claim?

> 

## Ablations

| Ablation | Question answered |
|---|---|
|  |  |

## Robustness / Stress Tests

- [ ] Different random seeds
- [ ] Different cohorts / datasets
- [ ] Distribution shift
- [ ] Reduced training data
- [ ] Label noise
- [ ] Missing features
- [ ] Alternative preprocessing
- [ ] Other:

## Reproducibility

- Code commit:
- Data versions:
- Environment / container:
- Seeds:
- Hardware:
- Runtime / compute budget:

## Results

> Fill after completion.

### Main table

| Method | Primary Metric | Uncertainty | Notes |
|---|---:|---:|---|
|  |  |  |  |

## Interpretation

What does the benchmark establish?

> 

What does it **not** establish?

> 

## Next Decision

> 
