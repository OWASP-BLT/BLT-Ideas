# BLT Project Ideas - Brief Overview

This document provides brief summaries of key BLT project ideas, with approximately three sentences describing each project's purpose and scope.

---

## 1. BLT-New: Core BLT Frontend Migration to Next.js/TypeScript

**Revamp BLT website with a fresh, modern design and separate components that don't support core value to create a clear, enjoyable user experience.** The project involves migrating the complete OWASP BLT platform from its current Django-based monolithic architecture to a modern, edge-optimized Next.js/TypeScript stack deployed on Cloudflare Pages. This comprehensive migration will transform Django template-based pages into React components while maintaining full feature parity, achieving sub-200ms global page load times, and positioning BLT as a reference implementation that attracts a new generation of contributors. The migration focuses on architecture modernization (90+ pages to Next.js App Router), performance optimization (Lighthouse score >95), developer experience improvements (TypeScript strict mode, reusable hooks), and comprehensive testing to ensure zero data loss and production-grade error handling.

---

## 2. BLT-Preflight: Pre-Contribution Security Intent & Risk Guidance

**Provide security intent and risk guidance before contributors submit code to prevent common mistakes and improve contributor understanding.** This pre-contribution advisory system helps contributors understand security expectations before opening a pull request by evaluating security context through issue labels, repository metadata, and historical patterns, then providing plain-language guidance linked to relevant documentation. The system includes optional contributor intent capture (planned work areas, components to modify, AI assistance usage), a maintainer visibility dashboard for early identification of risky contributions, and a learning feedback loop that refines guidance rules over time. BLT-Preflight operates on a purely advisory basis with no blocking or enforcement mechanisms, focusing on prevention and clarity to reduce maintainer workload and improve the quality of security contributions.

---

## 3. BLT-Rewards: BACON Rewards & Security Contribution Gamification

**Security contribution gamification with BACON tokens, badges, reputation tiers, and leaderboards to increase contributor retention and engagement.** The system listens for verified security contributions and awards rewards idempotently including BACON cryptocurrency tokens (with existing blockchain mint infrastructure), achievement badges for different security domains, progressive reputation tiers (Beginner → Expert), severity-weighted leaderboards, and a swag redemption marketplace where tokens convert to physical merchandise. Built with robust anti-gaming architecture (idempotent rewards, fraud detection, admin oversight), the platform includes comprehensive audit trails, an education bridge API layer for learning platform integration, and tokenomics analysis to ensure long-term sustainability. BLT-Rewards transforms security work into an engaging, progression-based experience that prioritizes impact over volume while enabling education platforms to leverage BLT contribution data for personalized learning paths.

---

## 4. NetGuardian: Distributed Autonomous Security Scanning Platform

**Community-powered security scanning platform with distributed scanning, real vulnerability detection, and responsible disclosure workflows.** NetGuardian replaces stubbed scanners with real vulnerability detection (XSS, SQLi, CSRF, security headers plus Semgrep SAST), introduces distributed scanning via secure volunteer CLI clients with local resource caps, and implements Zero-Trust encrypted ingestion where sensitive evidence stays encrypted end-to-end until authorized organization users decrypt it client-side. The platform includes result validation and false-positive filtering with confidence scoring, basic deduplication using fingerprints, triage-lite UI with evidence viewer and "Convert to Issue" workflow, security.txt detection for improved responsible disclosure, and professional remediation reports (CSV/PDF) for organizations. NetGuardian emphasizes accuracy through curated evaluation targets and rule tuning, privacy-preserving architecture with signed and timestamped submissions, and lower reviewer workload through normalized findings and streamlined triage.

---

## 5. Growth Griller: Sizzle-Powered Contributor Progress & AI-Guided Recommendations

**Time-aware contributor growth system that uses Sizzle time tracking to drive personal progress dashboards, AI-guided "what to work on next" recommendations, and proactive mentoring.** The system answers "where am I in my journey?" and "what should I work on next, and why?" for each contributor by tracking where they actually spent time (not just PR counts), inferring skill focus from Sizzle focus tags and issue labels, and providing meaningful contribution signals that distinguish BLT core work from low-value changes. AI-guided issue recommendations suggest concrete next steps with "why this issue," "what you'll learn," and estimated time based on Sizzle patterns, while the PR merged guidance mode proactively reaches out when PRs are merged with congratulations, growth profile updates, and next challenge suggestions. Growth Griller provides maintainers with capacity visibility (time investment by domain), smart issue-contributor matching, and insights into sustainable contribution pace, all powered by Celery async infrastructure for reliable LLM calls using Gemini free tier.

---

## 6. BLT University: Security-Focused Education Platform

**Security-focused education tool that teaches users about security through hands-on, code-centric labs and community-driven knowledge sharing.** The platform transforms BLT's existing theory-heavy labs into interactive exercises where learners analyze real vulnerable code, identify security flaws, explain exploitation scenarios, and apply secure fixes using a three-step workflow (Identify → Explain → Fix) with partial credit and progress tracking. BLT University establishes a safe, anonymized security intelligence pipeline that aggregates vulnerability patterns from BLT issues/PRs into public dashboards, monthly/quarterly reports with two-person approval workflows, and remediation playbooks that convert into mini interactive challenges. The unified architecture creates a feedback loop where real vulnerability patterns improve labs and playbooks, helping contributors learn security thinking inspired by OWASP Top 10 and CTF-style reasoning, with optional integration to badges/BACON gamification and future connections to NetGuardian findings for automatically mapped learning recommendations.

---

## 7. BLT-MCP: Model Context Protocol Server for Complete BLT Interface

**An interface to the BLT ecosystem enabling AI agents and developers to log bugs, triage issues, query data, and manage workflows from IDEs or chat interfaces.** BLT-MCP implements the Model Context Protocol (MCP) standard to provide comprehensive, AI-agent-friendly access to all aspects of BLT through three layers: Resources (read-only access to issues, repos, contributors, workflows, leaderboards, rewards via `blt://` URIs), Tools (actions like submit_issue, award_bacon, update_issue_status, add_comment), and Prompts (reusable task templates like triage_vulnerability, plan_remediation, review_contribution). The system uses JSON-RPC 2.0 over stdio or HTTP/SSE with OAuth 2.0/API key authentication, enabling natural integration with Claude Desktop, custom AI agents, and third-party tools without requiring custom API documentation since agents discover capabilities automatically. BLT-MCP positions BLT as an AI-agent-first platform with standardized protocol access that unifies fragmented REST/GraphQL endpoints, creates novel use cases (autonomous issue triage, automated reward distribution, workflow tracking), and synergizes with other BLT ideas by exposing RAG bot capabilities, AI-guided recommendations, reputation scores, and gamification data through a single consistent interface.

---

_Document created: February 2026_
_Source: OWASP BLT Ideas Repository_
