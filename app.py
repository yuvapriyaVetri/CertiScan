from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import boto3
from botocore.exceptions import ClientError

app = FastAPI(title="CertiScan")

templates = Jinja2Templates(directory="templates")

# =========================================================
# AWS S3 CONFIGURATION
# =========================================================

S3_BUCKET = "certiscan-certificates-2026-487615272741"
s3 = boto3.client("s3", region_name="us-east-1")


# =========================================================
# CERTISCAN DEMO CERTIFICATE REGISTRY
# =========================================================

CERTIFICATES = {

    # ===================== VALID =====================

    "VIT-2026-001": {
        "student": "Rahul Sharma",
        "institution": "VIT University",
        "program": "B.Tech Software Engineering",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "VIT-2026-002": {
        "student": "Priya Nair",
        "institution": "VIT University",
        "program": "B.Tech Computer Science",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "VIT-2026-003": {
        "student": "Arjun Kumar",
        "institution": "VIT University",
        "program": "B.Tech Information Technology",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "VIT-2026-004": {
        "student": "Meera Krishnan",
        "institution": "VIT University",
        "program": "B.Tech Software Engineering",
        "year": "2025",
        "status": "VALID",
        "risk": "LOW"
    },

    "VIT-2026-005": {
        "student": "Aditya Rao",
        "institution": "VIT University",
        "program": "B.Tech Electronics",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "STAN-2026-006": {
        "student": "Priya Kumar",
        "institution": "Stanford University",
        "program": "MS Computer Science",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "STAN-2026-007": {
        "student": "Daniel Thomas",
        "institution": "Stanford University",
        "program": "MS Data Science",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "OXF-2026-008": {
        "student": "Ananya Patel",
        "institution": "University of Oxford",
        "program": "MSc Computer Science",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "OXF-2026-009": {
        "student": "Rohan Mehta",
        "institution": "University of Oxford",
        "program": "MSc Artificial Intelligence",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "MIT-2026-010": {
        "student": "Karthik Iyer",
        "institution": "MIT",
        "program": "BSc Computer Science",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "MIT-2026-011": {
        "student": "Neha Singh",
        "institution": "MIT",
        "program": "MSc Technology",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "ABC-2026-012": {
        "student": "Vikram Das",
        "institution": "ABC University",
        "program": "B.Tech Information Technology",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },

    "ABC-2026-013": {
        "student": "Sneha Reddy",
        "institution": "ABC University",
        "program": "B.Tech Computer Science",
        "year": "2026",
        "status": "VALID",
        "risk": "LOW"
    },


    # ===================== REVOKED =====================

    "VIT-2026-014": {
        "student": "Arun Raj",
        "institution": "VIT University",
        "program": "B.Tech Computer Science",
        "year": "2026",
        "status": "REVOKED",
        "risk": "CRITICAL"
    },

    "VIT-2026-015": {
        "student": "Nisha Verma",
        "institution": "VIT University",
        "program": "B.Tech Software Engineering",
        "year": "2025",
        "status": "REVOKED",
        "risk": "CRITICAL"
    },

    "VIT-2026-016": {
        "student": "Sanjay Kumar",
        "institution": "VIT University",
        "program": "B.Tech Information Technology",
        "year": "2025",
        "status": "REVOKED",
        "risk": "CRITICAL"
    },

    "STAN-2026-017": {
        "student": "Michael Lee",
        "institution": "Stanford University",
        "program": "MS Computer Science",
        "year": "2025",
        "status": "REVOKED",
        "risk": "CRITICAL"
    },

    "OXF-2026-018": {
        "student": "David Wilson",
        "institution": "University of Oxford",
        "program": "MSc Computer Science",
        "year": "2025",
        "status": "REVOKED",
        "risk": "CRITICAL"
    },

    "MIT-2026-019": {
        "student": "Robert John",
        "institution": "MIT",
        "program": "BSc Computer Science",
        "year": "2025",
        "status": "REVOKED",
        "risk": "CRITICAL"
    },

    "ABC-2026-020": {
        "student": "Kevin Mathews",
        "institution": "ABC University",
        "program": "B.Tech Information Technology",
        "year": "2024",
        "status": "REVOKED",
        "risk": "CRITICAL"
    },


    # ===================== INVALID =====================

    "VIT-2026-021": {
        "student": "Sneha Patel",
        "institution": "VIT University",
        "program": "B.Tech Information Technology",
        "year": "2026",
        "status": "INVALID",
        "risk": "HIGH"
    },

    "VIT-2026-022": {
        "student": "Manoj Kumar",
        "institution": "VIT University",
        "program": "B.Tech Computer Science",
        "year": "2026",
        "status": "INVALID",
        "risk": "HIGH"
    },

    "STAN-2026-023": {
        "student": "Alex Brown",
        "institution": "Stanford University",
        "program": "MS Computer Science",
        "year": "2026",
        "status": "INVALID",
        "risk": "HIGH"
    },

    "OXF-2026-024": {
        "student": "Emma Davis",
        "institution": "University of Oxford",
        "program": "MSc Computer Science",
        "year": "2026",
        "status": "INVALID",
        "risk": "HIGH"
    },

    "MIT-2026-025": {
        "student": "Chris Martin",
        "institution": "MIT",
        "program": "BSc Computer Science",
        "year": "2026",
        "status": "INVALID",
        "risk": "HIGH"
    }
}


# =========================================================
# STATUS HISTORY
# =========================================================

def get_history(status):

    history = [
        {
            "date": "2026-01-10",
            "from": "ISSUED",
            "to": "VALID",
            "reason": "Certificate issued by institution"
        }
    ]

    if status == "REVOKED":

        history.append({
            "date": "2026-08-20",
            "from": "VALID",
            "to": "REVOKED",
            "reason": "Credential revoked by issuing institution"
        })

    elif status == "INVALID":

        history.append({
            "date": "2026-09-18",
            "from": "VALID",
            "to": "INVALID",
            "reason": "Certificate data mismatch detected"
        })

    return history


# =========================================================
# CHECK S3
# =========================================================

def check_s3(certificate_id):

    key = f"certificates/{certificate_id}.txt"

    try:

        s3.head_object(
            Bucket=S3_BUCKET,
            Key=key
        )

        return True

    except ClientError:

        return False

    except Exception:

        return False


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# =========================================================
# VERIFY CERTIFICATE
# =========================================================

@app.post("/verify", response_class=HTMLResponse)
async def verify(
    request: Request,
    certificate_id: str = Form(...)
):

    certificate_id = certificate_id.strip().upper()

    certificate = CERTIFICATES.get(certificate_id)

    # ---------------------------------------------
    # NOT FOUND
    # ---------------------------------------------

    if certificate is None:

        result = {
            "certificate_id": certificate_id,
            "status": "NOT FOUND",
            "risk": "UNKNOWN",
            "message": "Certificate ID is not registered in the CertiScan trusted registry.",
            "history": []
        }

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "certificate": result
            }
        )


    # ---------------------------------------------
    # FOUND
    # ---------------------------------------------

    result = certificate.copy()

    result["certificate_id"] = certificate_id

    result["history"] = get_history(
        certificate["status"]
    )

    result["s3_available"] = check_s3(
        certificate_id
    )


    # ---------------------------------------------
    # STATUS MESSAGE
    # ---------------------------------------------

    if result["status"] == "VALID":

        result["message"] = (
            "Certificate successfully verified against "
            "the trusted CertiScan registry."
        )

    elif result["status"] == "REVOKED":

        result["message"] = (
            "Certificate exists in the trusted registry "
            "but has been revoked by the issuing institution."
        )

    elif result["status"] == "INVALID":

        result["message"] = (
            "Certificate record indicates possible "
            "tampering or invalid credential data."
        )


    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "certificate": result
        }
    )


# =========================================================
# DIRECT VERIFICATION URL
# =========================================================

@app.get(
    "/verify/{certificate_id}",
    response_class=HTMLResponse
)
async def verify_direct(
    request: Request,
    certificate_id: str
):

    certificate_id = certificate_id.strip().upper()

    certificate = CERTIFICATES.get(certificate_id)

    # ---------------------------------------------
    # NOT FOUND
    # ---------------------------------------------

    if certificate is None:

        result = {
            "certificate_id": certificate_id,
            "status": "NOT FOUND",
            "risk": "UNKNOWN",
            "message": "Certificate ID is not registered in the CertiScan trusted registry.",
            "history": []
        }

    else:

        result = certificate.copy()

        result["certificate_id"] = certificate_id

        result["history"] = get_history(
            certificate["status"]
        )

        result["s3_available"] = check_s3(
            certificate_id
        )

        if result["status"] == "VALID":

            result["message"] = (
                "Certificate successfully verified against "
                "the trusted CertiScan registry."
            )

        elif result["status"] == "REVOKED":

            result["message"] = (
                "Certificate exists in the trusted registry "
                "but has been revoked by the issuing institution."
            )

        else:

            result["message"] = (
                "Certificate record indicates possible "
                "tampering or invalid credential data."
            )


    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "certificate": result
        }
    )


# =========================================================
# AWS HEALTH CHECK
# =========================================================


@app.get("/health")
@app.get("/scan")
async def scan_page(request: Request):

    certificate_ids = [
        "VIT-2026-001", "VIT-2026-002", "VIT-2026-003",
        "VIT-2026-004", "VIT-2026-005", "STAN-2026-006",
        "STAN-2026-007", "OXF-2026-008", "OXF-2026-009",
        "MIT-2026-010", "MIT-2026-011", "ABC-2026-012",
        "ABC-2026-013", "VIT-2026-014", "VIT-2026-015",
        "VIT-2026-016", "STAN-2026-017", "OXF-2026-018",
        "MIT-2026-019", "ABC-2026-020", "VIT-2026-021",
        "VIT-2026-022", "STAN-2026-023", "OXF-2026-024",
        "MIT-2026-025", "CERT-2026-026", "CERT-2026-027",
        "CERT-2026-028", "CERT-2026-029", "CERT-2026-030"
    ]

    return templates.TemplateResponse(
        "scan.html",
        {
            "request": request,
            "certificate_ids": certificate_ids
        }
    )
