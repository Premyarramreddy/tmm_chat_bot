# Telugu Matchmakers (TMM)

## RAG Knowledge Base Document – Home Page & Verification Flow

---

## 1. Purpose of This Document

This document is designed for **Retrieval-Augmented Generation (RAG)** systems.

It provides structured, reliable knowledge so that AI assistants can:

* Answer user questions correctly
* Guide users through onboarding
* Enforce platform rules
* Avoid hallucination

This document must be used as the **primary source** for homepage and verification-related queries.

---

## 2. User Onboarding Process

### 2.1 Entry Point

After Sign Up or Sign In, every user enters the onboarding flow.

### 2.2 Mandatory Sequence

Users must complete steps in the following order:

1. Profile Setup (First Mandatory Step)
2. Profile Verification (Second Mandatory Step)
3. Verified Status (Full Access)

Users cannot skip steps.

---

## 3. Profile Setup Rules

### 3.1 Requirement

* Profile Setup is mandatory for all users.
* It must be completed immediately after signup.

### 3.2 Access Restriction

If Profile Setup is incomplete:

* User remains Unverified
* Verification is hidden
* All major features are blocked
* User is redirected to Profile Setup

---

## 4. Profile Verification Rules

### 4.1 Availability

* Profile Verification becomes available only after Profile Setup is completed.

### 4.2 Requirement

* Verification is mandatory for platform access.

### 4.3 Access Restriction

If Verification is incomplete:

* User remains Unverified
* Profile is invisible to others
* All features remain restricted
* User is redirected to Verification

---

## 5. User Status Classification

| Status     | Setup Complete | Verification Complete | Access Level |
| ---------- | -------------- | --------------------- | ------------ |
| Unverified | No / Yes       | No                    | Limited      |
| Verified   | Yes            | Yes                   | Full         |

---

## 6. Visibility Policy

Until both steps are completed:

* User profile is hidden from:

  * Search
  * Recommendations
  * Online Profiles
  * Popular Matches
* Other users cannot view the profile

Only Verified users are publicly visible.

---

## 7. Homepage Feature Access Rules

When an Unverified user clicks any homepage feature, the system must check status.

### 7.1 Validation Logic

```
IF profile_setup_complete == false:
    Redirect → Profile Setup
ELSE IF verification_complete == false:
    Redirect → Profile Verification
ELSE:
    Allow Access
```

---

## 8. Homepage Features Reference

### 8.1 Search

Allows searching by:

* Country
* State
* City
* Community
* Sub-community
* First Name

Restricted for Unverified users.

---

### 8.2 Notifications

* Bell icon in homepage header
* Shows system and user notifications
* Blocked until verification

---

### 8.3 Online Profiles

* 🟢 Green: Online
* 🟠 Orange: Recently Online

Only visible to Verified users.

---

### 8.4 Recommended Profiles

* Displays ~10 profiles
* Horizontal scrolling
* Opens full profile on click
* “See All” → Matches Page

Verified access only.

---

### 8.5 TMM Exclusives

| Feature                 | Visibility Rule              |
| ----------------------- | ---------------------------- |
| Profile Setup           | Visible if incomplete        |
| Profile Verification    | Visible if incomplete        |
| Partner Preferences     | Available after verification |
| Compatibility Questions | Available after verification |
| Compare Profiles        | Available after verification |
| Book Appointment        | Available after verification |

---

### 8.6 Popular Matches

* Trending profiles
* ~10 profiles
* Horizontal scroll
* “See All” → Matches Page

Verified access only.

---

## 9. AI Assistant Response Rules (For RAG)

When answering users, the AI must:

1. Check user status first
2. Follow onboarding sequence
3. Never allow skipping steps
4. Never claim access without verification
5. Always redirect to pending step

---

## 10. Standard RAG Answers (Templates)

### 10.1 If Profile Setup Is Pending

"Please complete your Profile Setup first. After that, you can proceed with verification and access all features."

---

### 10.2 If Verification Is Pending

"Your profile setup is complete. Please finish Profile Verification to unlock all features."

---

### 10.3 If User Is Verified

"Your account is verified. You can now access all features and browse matches."

---

## 11. System Enforcement Policy

* No exceptions to onboarding rules
* No partial access
* No visibility without verification
* No manual overrides without admin approval

---

## 12. Document Usage

This document must be:

* Indexed in vector database
* Used as primary retrieval source
* Updated when policies change
* Version-controlled

---

End of RAG Knowledge Base Document
