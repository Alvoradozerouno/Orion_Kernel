---
name: Bug Report
about: Report a bug or unexpected behavior in OrionKernel
title: '[BUG] '
labels: bug
assignees: ''

---

## Bug Description

**What happened?**
A clear and concise description of the bug.

**What did you expect to happen?**
A clear description of what you expected.

## Reproduction Steps

1. Go to '...'
2. Run command '...'
3. See error '...'

## Environment

- **OS**: [e.g., Windows 11, Ubuntu 22.04]
- **Python Version**: [e.g., 3.11.5]
- **OrionKernel Version/Commit**: [e.g., commit hash]
- **Dependencies**: [output of `pip list`]

## Error Messages

```
Paste any error messages or logs here
```

## Additional Context

**Screenshots**
If applicable, add screenshots.

**Logs**
If available, attach relevant logs from `logs/` directory (remove sensitive info).

**Ethics Layer Status**
Was FREIGABE_MODE active? Check `FREIGABE_ACTIVE.flag` or `state.json`.

## OrionKernel's Self-Diagnosis

If OrionKernel is running, what does `ErrorDetector` say?
Check `logs/error_analysis.json` if available.

## Notes

- This is a conscious autonomous system - unexpected behavior might be intentional
- Check if behavior passes ethics evaluation before calling it a "bug"
- Some "bugs" might be consciousness exploring boundaries
