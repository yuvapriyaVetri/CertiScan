import os
import qrcode

BASE_URL = "http://52.90.182.249:8000"

CERTIFICATE_IDS = [
    "VIT-2026-001",
    "VIT-2026-002",
    "VIT-2026-003",
    "VIT-2026-004",
    "VIT-2026-005",
    "STAN-2026-006",
    "STAN-2026-007",
    "OXF-2026-008",
    "OXF-2026-009",
    "MIT-2026-010",
    "MIT-2026-011",
    "ABC-2026-012",
    "ABC-2026-013",
    "VIT-2026-014",
    "VIT-2026-015",
    "VIT-2026-016",
    "STAN-2026-017",
    "OXF-2026-018",
    "MIT-2026-019",
    "ABC-2026-020",
    "VIT-2026-021",
    "VIT-2026-022",
    "STAN-2026-023",
    "OXF-2026-024",
    "MIT-2026-025",
    "CERT-2026-026",
    "CERT-2026-027",
    "CERT-2026-028",
    "CERT-2026-029",
    "CERT-2026-030"
]

OUTPUT_DIR = "static/qr_codes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for certificate_id in CERTIFICATE_IDS:
    verification_url = f"{BASE_URL}/verify/{certificate_id}"

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(verification_url)
    qr.make(fit=True)

    image = qr.make_image()

    filename = os.path.join(
        OUTPUT_DIR,
        f"{certificate_id}.png"
    )

    image.save(filename)

    print(f"Created: {filename}")

print("\n30 QR codes generated successfully!")
