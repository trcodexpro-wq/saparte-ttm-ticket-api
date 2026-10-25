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

    search = request.args.get(
        "search", ""
    ).strip().lower()

    tickets = list(TICKETS.values())

    if search:
        tickets = [
            ticket for ticket in tickets
            if search in ticket["ticketId"].lower()
            or search in ticket["title"].lower()
        ]

    return jsonify({
        "tickets": tickets,
        "total": len(tickets)
    }), 200


@app.get("/api/tickets/<ticket_id>")
def get_ticket(ticket_id):

    ticket = TICKETS.get(ticket_id.upper())

    if ticket is None:
        return jsonify({
            "ticketId": ticket_id,
            "exists": False,
            "message": "Ticket not found"
        }), 404

    return jsonify({
        **ticket,
        "exists": True
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
