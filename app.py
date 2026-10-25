import os
import re
from flask import Flask, jsonify, request

app = Flask(__name__)


TICKETS = {
    "INC-1842": {
        "ticketId": "INC-1842",
        "title": "MM SAS Onay Geliştirmesi",
        "status": "IT_APPROVED"
    },
    "INC-2026": {
        "ticketId": "INC-2026",
        "title": "Malzeme Ana Veri Kontrolü",
        "status": "IN_PROGRESS"
    },
    "INC-3001": {
        "ticketId": "INC-3001",
        "title": "Eski Servis Hatası",
        "status": "CANCELLED"
    },
    "INC-4001": {
        "ticketId": "INC-4001",
        "title": "FI Rapor Geliştirmesi",
        "status": "PENDING_IT_APPROVAL"
    },
    "INC-5001": {
        "ticketId": "INC-5001",
        "title": "Satınalma Onay Akışı",
        "status": "BUSINESS_TESTING"
    },
    "INC-6001": {
        "ticketId": "INC-6001",
        "title": "Üretim Planlama Geliştirmesi",
        "status": "BUSINESS_APPROVED"
    },
    "INC-7001": {
        "ticketId": "INC-7001",
        "title": "Depo Yönetimi Geliştirmesi",
        "status": "TEST_REJECTED"
    }
}


@app.get("/")
def home():
    return jsonify(service="SAPARTE TTM Ticket Mock API", version="1.0", endpoints=["GET /health", "GET /api/tickets/<ticket_id>"])

@app.get("/health")
def health():
    return jsonify(status="ok")

# Mevcut Flask uygulamasına eklenecek endpoint

@app.get("/api/tickets")
def get_tickets():
    tickets = [
        {
            "ticketId": "INC-1842",
            "title": "MM SAS Onay Geliştirmesi",
            "status": "OPEN",
            "sapTransportAllowed": True
        },
        {
            "ticketId": "INC-2026",
            "title": "Malzeme Ana Veri Kontrolü",
            "status": "IN_PROGRESS",
            "sapTransportAllowed": True
        },
        {
            "ticketId": "INC-3001",
            "title": "Eski Servis Hatası",
            "status": "CLOSED",
            "sapTransportAllowed": False
        }
    ]

    search = request.args.get("search", "").strip().lower()
    allowed_only = request.args.get(
        "allowedOnly", "true"
    ).lower() == "true"

    if search:
        tickets = [
            t for t in tickets
            if search in t["ticketId"].lower()
            or search in t["title"].lower()
        ]

    if allowed_only:
        tickets = [
            t for t in tickets
            if t["sapTransportAllowed"]
        ]

    return jsonify({
        "tickets": tickets,
        "total": len(tickets)
    }), 200

@app.get("/api/tickets/<ticket_id>")
def get_ticket(ticket_id):
    ticket_id = ticket_id.upper().strip()
    if not re.fullmatch(r"INC-[0-9]{1,24}", ticket_id):
        return jsonify(ticketId=ticket_id, exists=False, error="INVALID_FORMAT", message="Expected INC-1234"), 400
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return jsonify(ticketId=ticket_id, exists=False, error="NOT_FOUND", message="Ticket not found"), 404
    return jsonify(ticketId=ticket_id, exists=True, **ticket), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
