# Top 5 GSoC Project Ideas for OWASP BLT 2026

**Ranking Criteria:**
- **Cybersecurity Impact:** Significant contribution to the cybersecurity industry
- **Scope:** 350 hours of work considering heavy AI assistance
- **Core Alignment:** True to BLT's core mission of finding and fixing bugs (UX/security/all types) in websites, repositories, projects, or apps

**Note:** This document ranks the top 5 GSoC projects (#1-#5) with the highest scores across all criteria, plus one honorable mention (#6) that provides valuable gamification infrastructure for the community.

---

## 🥇 Rank #1: Idea G — NetGuardian: Distributed Autonomous Security Scanning & Validation Platform

**Why This Ranks #1:**

**Cybersecurity Impact (10/10):**
- Replaces demo/stub scanners with **real vulnerability detection** (XSS, SQLi, CSRF, security headers, SAST)
- Introduces **distributed scanning** via volunteer CLI clients, democratizing security research
- Implements **Zero-Trust encrypted ingestion** protecting sensitive vulnerability data end-to-end
- Enables **autonomous discovery** from Certificate Transparency logs, GitHub, and blockchain
- Improves **responsible disclosure workflows** with security.txt detection and professional remediation reports
- Directly addresses real-world vulnerabilities at scale — the heart of cybersecurity defense

**AI Assistance Optimization (9/10):**
- AI can accelerate: UI components, API endpoints, detection rule templates, report generation
- Human expertise needed for: Detection logic tuning, false positive reduction, security validation
- Estimated 350 hours with AI: **Feasible** (90h foundation + 110h CLI + 90h quality + 60h disclosure/pilot)
- AI particularly helpful: Semgrep rule expansion, validation logic, CSV/PDF report generation, triage UI components

**Core BLT Alignment (10/10):**
- **Perfect alignment**: This IS bug finding and fixing — the core of BLT
- Finds real security bugs through distributed scanning
- Validates findings to reduce false positives
- Provides remediation guidance to fix bugs
- Supports responsible disclosure for discovered vulnerabilities
- Scales BLT's core mission through community-powered scanning

**Key Deliverables:**
1. Real detection pack (web vulns + Semgrep SAST)
2. Zero-Trust encrypted submission system
3. Volunteer CLI client for distributed scanning
4. Normalized finding schema with dedup and validation
5. Triage-lite UI with evidence viewer and issue conversion
6. Security.txt detection and disclosure helpers
7. Professional remediation reports (CSV/PDF)

**Impact Statement:**
NetGuardian transforms BLT from a bug reporting tool into an active, distributed vulnerability discovery platform. It directly finds security issues at scale while maintaining privacy through encryption, giving the cybersecurity community a powerful, ethical scanning platform.

---

## 🥈 Rank #2: Idea M — CVE Remediation Pipeline

**Why This Ranks #2:**

**Cybersecurity Impact (9/10):**
- Bridges the critical gap between "vulnerability found" and "confidently fixed"
- **AI-powered fix verification** ensures root causes are actually addressed, not just symptoms
- Identifies **related vulnerability patterns** elsewhere in codebases
- Reduces false confidence in incomplete fixes that leave systems vulnerable
- Emits verified remediation signals for reward systems, incentivizing quality fixes
- Scalable verification system addresses the growing volume of vulnerability reports

**AI Assistance Optimization (10/10):**
- **Perfect fit for AI**: Code diff analysis, pattern recognition, similarity detection
- AI excels at: Verifying fix completeness, finding similar patterns, generating remediation summaries
- Human-in-loop maintained through dashboard for oversight and override
- Gemini free tier sufficient for verification tasks
- Estimated 350 hours with AI: **Highly feasible** (40h webhooks + 50h model + 70h AI + 80h dashboard + 30h integration + 80h testing)
- AI dramatically reduces what would be manual code review work

**Core BLT Alignment (9/10):**
- **Strong alignment**: Ensures bugs are truly fixed, not just marked as fixed
- Complements bug discovery (Idea A/G) with quality assurance
- Lifecycle management from discovery → fix → verification
- Sits on top of core bug logging functionality
- Minor deduction: Doesn't find new bugs, but ensures existing ones are properly resolved

**Key Deliverables:**
1. Webhook ingestion from discovery systems (Idea A/G)
2. Remediation lifecycle state machine (discovered → verified)
3. AI verification service analyzing fix completeness and patterns
4. Remediation dashboard for maintainer oversight
5. Related pattern detection across codebase
6. Verified event emission to reward systems
7. Human-in-loop confirmation/override interface

**Impact Statement:**
CVE Remediation Pipeline solves the critical "is it really fixed?" problem in cybersecurity. By using AI to verify fixes are complete and identifying similar vulnerable patterns, it raises the bar for security remediation quality across the industry.

---

## 🥉 Rank #3: Idea H — BLT Growth: Sizzle-First Contributor Progress & AI-Guided Issue Recommendation

**Why This Ranks #3:**

**Cybersecurity Impact (7/10):**
- **Indirect but significant**: Improves quality and alignment of security contributions
- AI-guided recommendations direct contributors to **meaningful security work** vs. low-value PRs
- Reduces "AI slop" and gaming, focusing effort on real bug fixes
- Helps maintainers identify contributors with relevant security expertise
- Sustainable pace tracking reduces burnout, keeping security talent engaged
- Progress tracking emphasizes **quality over quantity** in security contributions

**AI Assistance Optimization (9/10):**
- AI perfectly suited for: Recommendation generation, skill analysis, learning path suggestions
- Gemini free tier ideal for personalized guidance
- AI accelerates: Dashboard UI, analytics visualization, notification systems
- Celery infrastructure for async LLM calls handles scaling
- Estimated 350 hours with AI: **Feasible** with clear phase breakdown
- Unique value: Proactive PR-merged guidance provides "AI mentor" experience

**Core BLT Alignment (8/10):**
- **Good alignment**: Focuses contributor effort on BLT core (bug/security/logging)
- "Meaningful contribution signal" measures alignment with bug logging mission
- Helps filter out peripheral PRs to focus on bug finding/fixing
- Sizzle-first approach tracks real investment in security work
- Minor deduction: Infrastructure project rather than direct bug work

**Key Deliverables:**
1. Sizzle-based progress tracker showing time-aware growth journey
2. AI-guided issue recommendations with "why" and "what you'll learn"
3. PR merged guidance system (proactive mentoring)
4. Skill focus inference from time tracking and issue labels
5. Maintainer capacity visibility and smart issue-contributor matching
6. Sustainable pace analysis and re-engagement nudges
7. Celery async infrastructure for reliable LLM integration

**Impact Statement:**
BLT Growth tackles the quality crisis in open source security contributions. By using time tracking and AI guidance to focus contributors on meaningful security work, it raises the overall quality of bug discovery and fixing efforts.

---

## 🎖️ Rank #4: Idea E — PR Readiness & Security Dashboard

**Why This Ranks #4:**

**Cybersecurity Impact (8/10):**
- **Comprehensive security visibility** across PRs with SAST, secret scanning, and dependency checks
- Correlates security findings with PR changes for **context-aware risk assessment**
- **Security-aware PR states** (READY, ACTION_REQUIRED, BLOCKED) prevent vulnerable code from merging
- Maintainer dashboard highlights **risky PRs** and unresolved security warnings
- Reduces false positives by prioritizing findings affecting changed code paths
- Provides clear remediation hints with links and guidance

**AI Assistance Optimization (9/10):**
- AI can accelerate: Dashboard UI, comment classification, reviewer intent detection, pattern recognition
- CI/CD aggregation and discussion threading are well-suited for AI automation
- Security signal correlation benefits from ML-based prioritization
- Estimated 350 hours with AI: **Highly feasible** with 16-week phased timeline
- Human-in-loop maintained through maintainer review and override capabilities
- Clear scope boundaries prevent feature creep

**Core BLT Alignment (8/10):**
- **Strong alignment**: Prevents bugs and security issues from reaching production
- Surfaces security risks early in the PR review process
- Helps maintainers make faster, safer merge decisions
- Reduces review friction by aggregating all signals in one place
- Minor deduction: Pre-merge prevention rather than post-deployment bug discovery
- Still core to mission: finding and fixing issues before they cause harm

**Key Deliverables:**
1. CI/CD check-run aggregation from GitHub Actions and other tools
2. PR discussion analysis with actionable vs non-actionable classification
3. Reviewer intent detection (blocking, needs changes, suggestion, nitpick)
4. Security tool result integration (SAST, secrets, dependency checks)
5. Security finding correlation with changed files and lines
6. Security-aware PR readiness states with blocking rules
7. Maintainer dashboard with high-risk PR queues and filters
8. Audit trail for PR readiness and security status changes

**Impact Statement:**
PR Readiness & Security Dashboard gives maintainers and contributors a single, actionable view of PR health and security posture. By aggregating CI/CD, security signals, and review context, it reduces merge risks and helps teams ship secure code faster.

---

## 🏅 Rank #5: BLT Core Website Optimization & Modularization

**Why This Ranks #5:**

**Cybersecurity Impact (7/10):**
- **Reduces attack surface** by splitting monolithic website into focused, minimal components
- Improves **security posture** through isolated deployment of core bug logging features
- Enables faster **security patches** on individual modules without full site deployment
- **Simplified codebase** makes security audits and vulnerability detection easier
- Cloudflare Workers and GitHub Pages provide **built-in DDoS protection** and CDN security
- Focuses resources on hardening BLT Core (bug submission, tracking, disclosure)

**AI Assistance Optimization (9/10):**
- AI excels at: Code modularization, dependency analysis, component extraction
- Perfect for: Automated refactoring, build configuration, deployment pipelines
- Can accelerate: UI component splitting, API endpoint separation, routing logic
- Estimated 350 hours with AI: **Highly feasible** with modularization automation
- AI-powered dead code elimination and dependency tree optimization
- Tooling generation for multi-repo management and cross-repo updates

**Core BLT Alignment (9/10):**
- **Strong alignment**: Focuses on optimizing BLT Core (bug logging) functionality
- Removes peripheral features that dilute the core mission
- Makes bug submission, tracking, and remediation workflows faster and more reliable
- Improves contributor experience through simplified, focused interface
- Separated repos enable independent scaling of core vs. auxiliary features
- Minor deduction: Infrastructure work, but directly serves core bug logging mission

**Key Deliverables:**
1. **BLT Core extraction:** Bug submission, tracking, disclosure, remediation (primary repo)
2. **Modular deployments:** Separate GitHub Pages / Cloudflare Workers apps per module
3. **Feature categorization:** Identify core vs. auxiliary features through data analysis
4. **Shared component library:** Common UI components across separated modules
5. **API gateway:** Unified authentication and routing layer for separated services
6. **Migration documentation:** Step-by-step guide for moving features between repos
7. **Performance benchmarks:** Sub-200ms response times for core bug logging flows
8. **Deployment automation:** CI/CD pipelines for each separated module

**Impact Statement:**
BLT Core Website Optimization transforms the platform from a feature-heavy monolith into focused, security-hardened microservices. By isolating core bug logging functionality and deploying on lightweight infrastructure (Cloudflare Workers, GitHub Pages), it delivers faster performance, improved security, and easier maintenance for the features that matter most.

**Architecture Vision:**
```
BLT Ecosystem (Separated Repos):
├── blt-core (Cloudflare Workers)          ← Bug submission, tracking, disclosure
├── blt-rewards (GitHub Pages)             ← BACON, badges, leaderboards
├── blt-education (GitHub Pages)           ← Security learning tracks
├── blt-community (GitHub Pages)           ← Forums, discussions, blog
└── blt-api-gateway (Cloudflare Workers)   ← Unified auth & routing
```

---

## 🎗️ Rank #6: Idea B — Security Contribution Gamification & Recognition (with Light C Education Bridge)

**Why This Ranks #6:**

**Cybersecurity Impact (7/10):**
- **Incentivizes security contributions** through BACON tokens, badges, and reputation
- Quality-weighted leaderboards prioritize **impact over volume**
- Education bridge (Light C) connects achievements to learning platforms
- Fraud detection and anti-gaming controls maintain integrity
- Challenges and competitions focus community on security priorities
- Tokenomics review ensures sustainable long-term incentive model

**AI Assistance Optimization (7/10):**
- AI can accelerate: UI components, dashboard visualizations, API endpoints, badge system
- Blockchain integration and tokenomics require careful manual design
- Some complex logic (fraud detection, severity weighting) needs human expertise
- Estimated 350 hours with AI: **Challenging but possible** with 12-week timeline
- Note: README indicates this may be 400+ hours if "light C" is fully built out
- Risk: Scope creep into full education platform

**Core BLT Alignment (6/10):**
- **Indirect alignment**: Rewards bug work but doesn't find/fix bugs directly
- Assumes feed of verified contributions from other systems
- Infrastructure/recognition layer rather than core bug discovery
- Education bridge is peripheral to main bug logging mission
- Value: Motivates others to do bug work, but isn't bug work itself
- Deduction: Furthest from "finding and fixing bugs" among top 5

**Key Deliverables:**
1. BACON Web3 token integration and distribution system
2. Tokenomics audit and optimization recommendations
3. Swag marketplace for token redemption
4. Achievement badge system (50+ badges)
5. Severity-weighted leaderboards (multiple views)
6. Reputation tier progression (Beginner → Security Leader)
7. Education bridge APIs for external platform integration
8. Fraud detection and admin audit tools

**Impact Statement:**
Security Contribution Gamification creates a sustainable motivation layer for the cybersecurity community. By rewarding quality security work with tokens and recognition, it can drive long-term engagement with bug discovery and remediation efforts.

---

## Summary Comparison Matrix

| Rank | Idea | Cyber Impact | AI Feasibility | Core Alignment | Total Score |
|------|------|--------------|----------------|----------------|-------------|
| **#1** | **NetGuardian (G)** | 10/10 | 9/10 | 10/10 | **29/30** |
| **#2** | **CVE Remediation (M)** | 9/10 | 10/10 | 9/10 | **28/30** |
| **#3** | **BLT Growth (H)** | 7/10 | 9/10 | 8/10 | **24/30** |
| **#4** | **PR Readiness & Security (E)** | 8/10 | 9/10 | 8/10 | **25/30** |
| **#5** | **BLT Core Website Optimization** | 7/10 | 9/10 | 9/10 | **25/30** |
| **#6** | **Gamification (B)** | 7/10 | 7/10 | 6/10 | **20/30** |

---

## Why These Top Ideas?

**What Made the Cut:**
1. **Direct security impact** — Finding, fixing, verifying vulnerabilities, or optimizing security-critical infrastructure
2. **AI acceleration** — Tasks that benefit significantly from AI assistance within 350 hours
3. **Core mission alignment** — True to bug logging, discovery, and remediation
4. **Implementable scope** — Realistic for GSoC timeframe with heavy AI assistance
5. **Industry impact** — Meaningful contribution to cybersecurity practices

**Top 5 Core Projects:**
The top 5 ranked ideas (#1-#5) represent the most impactful GSoC projects:
- **NetGuardian** and **CVE Remediation** directly find and fix bugs at scale
- **BLT Growth** ensures quality contributions focused on meaningful security work
- **PR Readiness & Security Dashboard** prevents bugs before they ship
- **BLT Core Website Optimization** streamlines and secures the core bug logging platform

These five create a comprehensive security pipeline while staying true to BLT's mission.

**Notable Exclusions:**

- **Idea K (Frontend Migration):** Valuable infrastructure modernization, but broader than BLT Core Website Optimization (#5) which focuses specifically on modularizing and trimming to core bug logging features
- **Idea E (Extended):** Security Remediation Triage is now covered by updated Idea E (#4) which includes comprehensive security dashboard capabilities
- **Idea A (CVE Detection):** Good but overlaps with Idea G; NetGuardian is more comprehensive with distributed scanning
- **Idea F (Reputation Graph):** Complex scoring system, less direct bug impact than chosen ideas
- **Idea I (First-Time Contributor):** Important for onboarding but peripheral to core security work
- **Idea Z (BLT-MCP):** Integration layer, not direct security contribution; enables other tools rather than finding bugs
- **Idea J (Cybersecurity News API):** News aggregation, not bug discovery; more about awareness than action

---

## Recommendation for GSoC 2026

For **maximum cybersecurity industry impact** while staying true to BLT's bug logging core within a 350-hour scope with AI assistance:

**Primary Recommendation: NetGuardian (G)** — This is the flagship project. It transforms BLT into an active vulnerability discovery platform with real detection capabilities, distributed community scanning, and responsible disclosure. This IS bug logging at scale.

**Strong Secondary: CVE Remediation Pipeline (M)** — Perfect complement to discovery. Ensures the bugs that are found are actually fixed properly. AI-native design makes it highly implementable in 350 hours.

**Quality Focus: BLT Growth (H)** — Addresses the AI slop and contribution quality crisis. Focuses human effort on meaningful security work through intelligent guidance.

**Security Gate: PR Readiness & Security Dashboard (E)** — Prevents vulnerable code from merging by providing comprehensive security visibility across PRs with SAST, secret scanning, and intelligent triage.

**Infrastructure Focus: BLT Core Website Optimization** — Streamlines the platform by extracting and optimizing core bug logging features into focused, security-hardened microservices on Cloudflare Workers and GitHub Pages.

**Complete Pipeline:**
1. **Find bugs at scale** (NetGuardian)
2. **Fix them properly** (CVE Remediation)
3. **Guide contributors to quality work** (BLT Growth)
4. **Prevent issues before merge** (PR Security Dashboard)
5. **Optimize core platform** (Website Optimization)

All five are achievable in 350-hour scopes with heavy AI assistance and deliver direct impact on BLT's core mission.

---

_This ranking reflects BLT's core mission: helping the cybersecurity industry find and fix bugs effectively. The top 5 ideas deliver the most direct impact on actual vulnerability discovery, remediation, and platform optimization._
