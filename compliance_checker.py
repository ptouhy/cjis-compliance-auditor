from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
#import openai  # For LLM integration when ready

# Defines the possible outcomes of a compliance check
class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    MISSING = "missing"
    PENDING_REVIEW = "pending_review"

# A data structure (using dataclass for brevity) to hold the details of a single CJIS rule
@dataclass
class CJISRequirement:
    """Individual CJIS requirement with exact policy text"""
    id: str                 # Unique identifier for the rule (e.g., "5.6.3.2.1")
    section: str            # CJIS section number (e.g., "5.6.3.2")
    title: str              # Short, human-readable title for the rule
    requirement_text: str   # The official text of the CJIS requirement
    critical: bool = True   # Flag indicating if the requirement is critical
    keywords: List[str] = None # List of keywords used for basic analysis

# A data structure to hold the result of checking one requirement against a policy
@dataclass
class ComplianceCheck:
    """Result of checking one requirement against agency policy"""
    requirement: CJISRequirement # The rule that was checked
    status: ComplianceStatus     # The outcome (Compliant, Non-Compliant, etc.)
    confidence: float            # How confident the analysis is (0.0 to 1.0)
    evidence_text: str           # Snippet from the agency policy used as evidence
    issues: List[str]            # List of specific problems found
    suggestions: List[str]       # List of suggestions for fixing the issues
    auditor_confirmed: bool = False # Flag for auditor review workflow
    auditor_notes: str = ""         # Notes added by the auditor

# The main class responsible for performing the compliance analysis
class CJISComplianceChecker:
    """
    Systematic checker that validates agency policies against CJIS requirements.
    Designed for auditor oversight and confirmation workflow.
    """
    
    # Constructor: Runs when a new CJISComplianceChecker is created
    def __init__(self):
        # Load all the CJIS rules from the internal method into memory
        self.cjis_requirements = self._load_cjis_requirements()
        # Placeholder for an LLM client (e.g., OpenAI, Gemini) - not used yet
        self.llm_client = None
        
    # Internal method to define all the CJIS rules known by this checker
    def _load_cjis_requirements(self) -> Dict[str, List[CJISRequirement]]:
        """Load all CJIS requirements organized by section key (e.g., 'authenticator_management')."""
        # Returns a dictionary where keys are section names and values are lists of CJISRequirement objects
        return {
            "authenticator_management": [
                # ... (list of CJISRequirement objects for this section) ...
                CJISRequirement(
                    id="5.6.3.2.1",
                    section="5.6.3.2",
                    title="Define Initial Authenticator Content",
                    requirement_text="Agencies shall define initial authenticator content for authenticators defined by the organization.",
                    keywords=["initial", "authenticator", "content", "define", "organization"]
                ),
                # ... (other requirements for authenticator_management) ...
            ],

            "media_protection": [
                # ... (list of CJISRequirement objects for this section) ...
                CJISRequirement(
                    id="5.10.1.1",
                    section="5.10.1",
                    title="Media Access Control",
                    requirement_text="The information system shall restrict access to digital and non-digital media to authorized individuals.",
                    keywords=["restrict access", "media", "authorized", "individuals"]
                ),
                # ... (other requirements for media_protection) ...
            ],
            
            "access_control": [
                 # ... (list of CJISRequirement objects for this section) ...
                CJISRequirement(
                    id="5.2.1",
                    section="5.2",
                    title="Least Privilege Access",
                    requirement_text="Agencies shall enforce the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) which are necessary to accomplish assigned tasks.",
                    keywords=["least privilege", "authorized access", "need-to-know", "need-to-share", "role-based"]
                ),
                # ... (other requirements for access_control) ...
            ],

            "audit_and_accountability": [
                 # ... (list of CJISRequirement objects for this section) ...
                CJISRequirement(
                    id="5.4.1",
                    section="5.4",
                    title="Audit Log Generation",
                    requirement_text="The information system shall generate audit records containing information that establishes what type of event occurred, when the event occurred, where the event occurred, the source of the event, the outcome of the event, and the identity of any user/subject associated with the event.",
                    keywords=["audit records", "generate", "event", "when", "where", "source", "outcome", "identity", "user"]
                ),
                # ... (other requirements for audit_and_accountability) ...
            ],

            "physical_protection": [
                 # ... (list of CJISRequirement objects for this section) ...
                 CJISRequirement(
                    id="5.9.1",
                    section="5.9",
                    title="Physical Access Control",
                    requirement_text="The agency shall limit physical access to information systems, equipment, and the respective operating environments to authorized individuals.",
                    keywords=["limit", "physical access", "systems", "equipment", "authorized individuals"]
                ),
                # ... (other requirements for physical_protection) ...
            ]
        }
    
    # Public method called by main.py to start an analysis for a specific section
    def check_section(self, section_name: str, agency_policy_text: str) -> List[ComplianceCheck]:
        """
        Check all requirements in a given CJIS section against the provided agency policy text.
        """
        # Check if the requested section name is valid (exists in our loaded requirements)
        if section_name not in self.cjis_requirements:
            raise ValueError(f"Unknown CJIS section: {section_name}")
            
        # Get the list of rules for the requested section
        requirements = self.cjis_requirements[section_name]
        compliance_checks = [] # List to store the results for each rule
        
        # Loop through each rule in the section
        for requirement in requirements:
            # Analyze this single rule against the policy text
            check = self._analyze_requirement(requirement, agency_policy_text)
            compliance_checks.append(check) # Add the result to our list
            
        # Return the list of all results for this section
        return compliance_checks
    
    # Internal method that decides whether to use LLM or keyword analysis
    def _analyze_requirement(self, requirement: CJISRequirement, agency_policy: str) -> ComplianceCheck:
        """
        Analyze a single requirement against the agency policy.
        Delegates to either LLM or keyword analysis based on availability.
        """
        if self.llm_client: # If an LLM client is configured (currently None)
            return self._llm_analysis(requirement, agency_policy)
        else: # Otherwise, use the basic keyword analysis
            return self._keyword_analysis(requirement, agency_policy)
    
    # Placeholder for future LLM-based analysis
    def _llm_analysis(self, requirement: CJISRequirement, agency_policy: str) -> ComplianceCheck:
        """LLM-powered semantic analysis (to be implemented later)."""
        prompt = f"""
        # ... (LLM prompt defined here) ...
        """
        # In the future, API call to LLM would happen here
        # For now, it just falls back to keyword analysis
        print("Note: LLM analysis not implemented, falling back to keyword analysis.")
        return self._keyword_analysis(requirement, agency_policy)
    
    # The current core analysis logic: basic keyword matching
    def _keyword_analysis(self, requirement: CJISRequirement, agency_policy: str) -> ComplianceCheck:
        """Performs a simple keyword-based analysis."""
        policy_lower = agency_policy.lower() # Convert policy to lowercase for case-insensitive matching
        issues = []
        suggestions = []
        evidence_text = ""
        
        # --- Find sentences relevant to the rule's keywords ---
        relevant_sentences = []
        sentences = agency_policy.split('.') # Basic sentence splitting
        for sentence in sentences:
            # Check if any of the rule's keywords appear in the sentence
            if any(keyword.lower() in sentence.lower() for keyword in requirement.keywords):
                relevant_sentences.append(sentence.strip())
        
        # Use the first couple of relevant sentences as evidence
        evidence_text = '. '.join(relevant_sentences[:2])
        
        # --- Determine compliance based on keyword coverage ---
        # Count how many of the rule's keywords are present in the policy
        keyword_matches = sum(1 for keyword in requirement.keywords 
                            if keyword.lower() in policy_lower)
        # Calculate a simple coverage percentage
        coverage = keyword_matches / len(requirement.keywords) if requirement.keywords else 0
        
        # Determine status based on coverage threshold (simple logic)
        if coverage >= 0.7 and len(relevant_sentences) > 0:
            status = ComplianceStatus.COMPLIANT
            confidence = min(0.85, coverage) # Cap confidence slightly below 1.0
        elif coverage >= 0.3:
            status = ComplianceStatus.NON_COMPLIANT
            confidence = 0.6
            issues.append(f"Partially addresses requirement but missing key elements")
            suggestions.append(f"Ensure policy explicitly addresses: {requirement.requirement_text}")
        else:
            status = ComplianceStatus.MISSING
            confidence = 0.3
            issues.append("No evidence found for this requirement")
            suggestions.append(f"Add policy section covering: {requirement.title}")
        
        # Create and return the ComplianceCheck result object
        return ComplianceCheck(
            requirement=requirement,
            status=status,
            confidence=confidence,
            evidence_text=evidence_text,
            issues=issues,
            suggestions=suggestions
            # auditor_confirmed defaults to False
        )
    
    # Method to format the raw analysis results into a structure the frontend expects
    def generate_audit_checklist(self, compliance_checks: List[ComplianceCheck]) -> Dict:
        """
        Generate a structured dictionary (checklist) from the compliance results,
        suitable for sending back as JSON to the frontend.
        """
        checklist = {
            # Summary statistics
            "summary": {
                "total_requirements": len(compliance_checks),
                "compliant": len([c for c in compliance_checks if c.status == ComplianceStatus.COMPLIANT]),
                "non_compliant": len([c for c in compliance_checks if c.status == ComplianceStatus.NON_COMPLIANT]),
                "missing": len([c for c in compliance_checks if c.status == ComplianceStatus.MISSING]),
                "pending_review": len([c for c in compliance_checks if not c.auditor_confirmed]) # All items initially require review
            },
            # List of critical issues (non-compliant or missing critical rules)
            "critical_issues": [c.__dict__ for c in compliance_checks # Convert dataclass to dict for JSON
                             if c.requirement.critical and c.status != ComplianceStatus.COMPLIANT],
            # List of all checks needing review (initially all checks)
            "requires_confirmation": [c.__dict__ for c in compliance_checks if not c.auditor_confirmed], # Convert dataclass to dict
            # Checks grouped by their specific CJIS subsection (e.g., "5.6.3.2")
            "by_section": {}
        }
        
        # Populate the by_section grouping
        for check in compliance_checks:
            section_id = check.requirement.section # Get the specific section ID (e.g., "5.6.3.2")
            if section_id not in checklist["by_section"]:
                checklist["by_section"][section_id] = []
            # Convert dataclass to dict before appending for JSON compatibility
            checklist["by_section"][section_id].append(check.__dict__)
        
        # Convert nested CJISRequirement objects within the lists to dictionaries as well
        for key in ["critical_issues", "requires_confirmation"]:
            for item in checklist[key]:
                item['requirement'] = item['requirement'].__dict__
        for section_key in checklist["by_section"]:
            for item in checklist["by_section"][section_key]:
                 item['requirement'] = item['requirement'].__dict__

        return checklist
    
    # --- Placeholder Methods for Future Features ---
    
    def confirm_finding(self, check_id: str, auditor_confirmed: bool, notes: str = ""):
        """(Future) Allow auditor to confirm or override findings."""
        # This would likely involve updating a database record in a full implementation
        pass
    
    def export_final_report(self, compliance_checks: List[ComplianceCheck]) -> Dict:
        """(Future) Generate a final compliance report after auditor review."""
        confirmed_checks = [c for c in compliance_checks if c.auditor_confirmed]
        # ... (logic to format a final report) ...
        return {} # Placeholder
    
    def _generate_prioritized_recommendations(self, checks: List[ComplianceCheck]) -> List[Dict]:
        """(Future) Generate prioritized list of recommendations based on findings."""
        recommendations = []
        # ... (logic to prioritize recommendations) ...
        return recommendations # Placeholder

# --- Example Usage Block ---
# This code runs only if you execute `python compliance_checker.py` directly
# It's useful for basic testing of the checker logic itself
def main():
    checker = CJISComplianceChecker()
    
    # Define a simple sample policy text for testing
    agency_policy = """
    METRO POLICE DEPARTMENT - AUTHENTICATOR MANAGEMENT POLICY
    Section 4.2: Access Control and Authentication
    All department personnel must use strong passwords containing at least 8 characters.
    Passwords must be changed every 90 days.
    New officers receive temporary login credentials during orientation.
    Default passwords must be changed upon first system login.
    Officers must immediately report lost ID badges to their supervisor.
    Personnel are prohibited from sharing login credentials.
    """
    
    try:
        # Run compliance check for a specific section
        compliance_results = checker.check_section("authenticator_management", agency_policy)
        
        # Generate the checklist dictionary
        audit_checklist = checker.generate_audit_checklist(compliance_results)
        
        # Print a simple summary to the console
        print("=== CJIS COMPLIANCE AUDIT CHECKLIST ===")
        print(f"Total Requirements: {audit_checklist['summary']['total_requirements']}")
        print(f"Compliant: {audit_checklist['summary']['compliant']}")
        print(f"Non-Compliant: {audit_checklist['summary']['non_compliant']}")
        print(f"Missing: {audit_checklist['summary']['missing']}")
        
        print("\n=== REQUIRES AUDITOR CONFIRMATION ===")
        # Print details for items requiring review
        for check in audit_checklist["requires_confirmation"]:
            # Access dictionary keys now since generate_audit_checklist converts them
            print(f"\n{check['requirement']['title']}") 
            print(f"Status: {check['status']}") # Status is already a string from Enum value
            print(f"Evidence: {check['evidence_text']}")
            print(f"Issues: {check['issues']}")
            print("[ ] Auditor Confirmed")
            
    except ValueError as e:
        print(f"Error: {e}") # Print section errors if they occur during testing

# Standard Python practice: Call the main() function if this script is run directly
if __name__ == "__main__":
    main()