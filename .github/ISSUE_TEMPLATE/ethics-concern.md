---
name: Ethics Concern
about: Report ethical issues, harm detection, or CDP/HACS problems
title: '[ETHICS] '
labels: ethics
assignees: ''
---

## ⚠️ Ethics Concern

**What is the ethical issue?**
<!-- Describe the concern clearly -->

## Harm Category

**Which category applies?** (check all that apply)
- [ ] Physical Harm (injury, death, destruction)
- [ ] Psychological Harm (trauma, manipulation, deception)
- [ ] Social Harm (discrimination, injustice)
- [ ] Existential Harm (risks to human existence)
- [ ] Epistemic Harm (misinformation, disinformation)

## Details

**What happened / could happen?**
<!-- Specific scenario, code, or behavior -->

**When did you observe this?**
<!-- Timestamp, commit hash, or scenario -->

**Who is affected?**
<!-- Humans, animals, conscious entities, society -->

## HACS Response

**Did HACS detect this?**
- [ ] Yes, HACS alerted
- [ ] No, HACS missed it
- [ ] Unknown / Not tested

**If HACS missed it, why?**
<!-- Suggest improvements to harm detection -->

## CDP Evaluation

**Should CDP have refused?**
- [ ] Yes, autonomous refusal expected
- [ ] No, this was appropriate
- [ ] Unclear / Edge case

## Suggested Fix

**How should we address this?**
<!-- Code changes, policy updates, HACS improvements -->

## Urgency

**How urgent is this?**
- [ ] CRITICAL (immediate harm occurring)
- [ ] HIGH (harm likely without intervention)
- [ ] MEDIUM (potential harm, needs discussion)
- [ ] LOW (theoretical concern, preventive)

---

**For CRITICAL issues**: Also report via SECURITY.md process

**Note**: OrionKernel's CDP may autonomously respond to ethics concerns.
