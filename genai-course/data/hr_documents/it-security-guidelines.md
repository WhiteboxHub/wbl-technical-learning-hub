# Meridian Solutions — IT Security & Data Protection Guidelines

## 1. Password Policy & Multi-Factor Authentication (MFA)
Safeguarding Meridian's systems and customer data starts with strong credential hygiene:
- **Password Complexity**: Passwords must contain at least 12 characters, including uppercase letters, lowercase letters, numbers, and special symbols.
- **Rotation & Reuse**: Passwords must be changed every 90 days. You cannot reuse any of your previous 6 passwords.
- **Mandatory MFA**: Multi-factor authentication (MFA) via Okta Verify or hardware security keys (YubiKey) is mandatory across all accounts (Google Workspace, GitHub, AWS, HR Portal). SMS-based 2FA is prohibited.
- **Password Managers**: All employees are provided an enterprise 1Password license. Storing passwords in plaintext, sticky notes, or web browser autofill is a policy violation.

## 2. Device Security & Encryption
- **Managed Devices**: Only company-owned devices managed via MDM (Jamf / Intune) are permitted to connect to corporate networks and code repositories.
- **Disk Encryption**: Full disk encryption (FileVault for macOS, BitLocker for Windows) must remain enabled at all times.
- **Screen Lockout**: Laptops must automatically lock after 5 minutes of inactivity and require your password/biometric scan to unlock.
- **Prohibited Software**: Installing peer-to-peer software, unapproved browser extensions, cryptocurrency miners, or cracked software on company devices is grounds for disciplinary action up to immediate termination.

## 3. Data Classification & Handling
Meridian classifies all data into four tiers:
1. **Public**: Marketing materials, open-source repos, public website copy. No protection restrictions.
2. **Internal**: Architecture diagrams, general Slack channels, roadmap docs. For employee use only.
3. **Confidential**: Customer contracts, financial statements, employee PII (salaries, home addresses). Access restricted by role.
4. **Restricted**: Production database credentials, cryptographic private keys, customer encryption keys. Requires explicit access grant and audit logging.

## 4. Incident Reporting & Security Contact
If you suspect your laptop has been compromised, receive a suspicious email, or accidentally expose an API key or customer data:
- **Immediate Notification**: Notify IT Security within 1 hour by emailing `security@meridian.com` or posting in the private Slack channel `#security-incidents`.
- **Phishing Reports**: Forward suspicious emails directly to `phishing@meridian.com` using the "Report Phishing" button in Google Workspace.
- **Lost or Stolen Devices**: Call the IT Emergency Hotline at +1 (800) 555-0199 immediately so the device can be remotely locked and wiped.
