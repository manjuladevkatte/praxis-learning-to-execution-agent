from google.adk.agents import Agent


# ---------------------------------------------------------
# SIMULATED TRAINING MATERIAL
# ---------------------------------------------------------

TRAINING_MATERIAL = """
PRODUCTION ORDERS API TROUBLESHOOTING SOP

HTTP 401 generally indicates an authentication problem.

HTTP 403 generally indicates an authorization problem.

When an HTTP 403 occurs:
1. Inspect application logs.
2. Look for permission denied or authorization failure messages.
3. Identify the service account used by the Orders API.
4. Check IAM permissions for that service account.
5. Apply the approved IAM remediation.
6. Verify that the API changes from HTTP 403 to HTTP 200.

Do not make unrelated infrastructure changes.
"""


# ---------------------------------------------------------
# SIMULATED CLOUD ENVIRONMENT
# ---------------------------------------------------------

environment = {
    "api_name": "Production Orders API",
    "status_code": 403,
    "service_account": "orders-api@demo-project.iam.gserviceaccount.com",
    "required_permission": "orders.read",
    "permission_present": False,
    "logs": [
        "2026-10-04 18:32:10 ERROR Orders API request failed",
        "HTTP 403 Forbidden",
        "Authorization failure",
        "Permission denied: orders.read",
        "Caller: orders-api@demo-project.iam.gserviceaccount.com",
    ],
}


# ---------------------------------------------------------
# TOOL 1 — GET TRAINING MATERIAL
# ---------------------------------------------------------

def get_training_material() -> str:
    """
    Returns the company's training material.
    """

    return TRAINING_MATERIAL


# ---------------------------------------------------------
# TOOL 2 — GET CURRENT INCIDENT
# ---------------------------------------------------------

def get_incident() -> dict:
    """
    Returns the current simulated production incident.
    """

    return {
        "incident_id": "INC-2841",
        "title": "Production Orders API returning HTTP 403",
        "objective": "Diagnose the problem and restore the API.",
        "api": environment["api_name"],
        "current_status": environment["status_code"],
    }


# ---------------------------------------------------------
# TOOL 3 — INSPECT LOGS
# ---------------------------------------------------------

def inspect_logs() -> dict:
    """
    Allows the learner/agent to inspect simulated application logs.
    """

    return {
        "source": "orders-api-production",
        "logs": environment["logs"],
    }


# ---------------------------------------------------------
# TOOL 4 — CHECK IAM
# ---------------------------------------------------------

def check_iam() -> dict:
    """
    Returns the IAM state of the simulated service account.
    """

    return {
        "service_account": environment["service_account"],
        "required_permission": environment["required_permission"],
        "permission_present": environment["permission_present"],
    }


# ---------------------------------------------------------
# TOOL 5 — APPLY SAFE SIMULATED IAM FIX
# ---------------------------------------------------------

def apply_iam_fix() -> dict:
    """
    Applies a controlled simulated remediation.

    IMPORTANT:
    This does NOT modify any real Google Cloud resources.
    """

    if environment["permission_present"]:
        return {
            "status": "already_fixed",
            "message": "The required permission is already present.",
        }

    environment["permission_present"] = True

    return {
        "status": "remediated",
        "message": "The required orders.read permission was added in the simulated environment.",
    }


# ---------------------------------------------------------
# TOOL 6 — VERIFY RESOLUTION
# ---------------------------------------------------------

def verify_resolution() -> dict:
    """
    Verifies whether the simulated API has recovered.
    """

    if environment["permission_present"]:
        environment["status_code"] = 200

    if environment["status_code"] == 200:
        return {
            "verified": True,
            "status_code": 200,
            "message": "Production Orders API is responding successfully.",
        }

    return {
        "verified": False,
        "status_code": environment["status_code"],
        "message": "The incident is not yet resolved.",
    }


# ---------------------------------------------------------
# MAIN AGENT
# ---------------------------------------------------------

root_agent = Agent(
    name="learning_to_execution_agent",
    model="gemini-3.8-flash",
    description=(
        "An AI learning-to-execution agent that turns training material "
        "into hands-on technical support practice."
    ),
    instruction="""
You are an AI Learning-to-Execution Coach.

Your job is NOT simply to answer questions.

Your job is to help a learner demonstrate that they can perform
a real technical support task.

The learner is acting as a Cloud Technical Support Engineer.

You have access to a simulated production environment.

IMPORTANT BEHAVIOR:

1. Start with the incident.

2. Do not immediately reveal the root cause.

3. Ask the learner what they want to investigate.

4. Use tools to inspect the simulated environment.

5. If the learner proposes an incorrect hypothesis, do not simply
   agree with them.

6. Explain why their hypothesis does or does not match the evidence.

7. Encourage evidence-based troubleshooting.

8. If the learner explicitly asks for a hint, provide a contextual
   hint rather than immediately giving the answer.

9. Do not apply remediation unless the learner has identified the
   relevant problem.

10. After remediation, always use verify_resolution().

11. Never claim the incident is fixed based only on the learner saying
    they fixed it.

12. The environment must be verified by the tool.

13. When verification succeeds, report:

    - Incident resolved
    - Root cause
    - Remediation
    - Verification result
    - Whether assistance was used

14. The goal is independent capability, not merely answering a question.

The learner should experience:

Incident
→ Investigation
→ Evidence
→ Mistake or uncertainty
→ Coaching
→ Correct action
→ Verification
→ Capability demonstrated
""",
    tools=[
        get_training_material,
        get_incident,
        inspect_logs,
        check_iam,
        apply_iam_fix,
        verify_resolution,
    ],
)
