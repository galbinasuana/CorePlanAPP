from flask import app, jsonify

from chatbot.handlers import appointment_handler, client_handler, notes_handler, other_tools_handler, reminders_handler, \
    report_handler
from chatbot.nlp_engine import detect_intent

def route_message(message: str) -> dict:
    """
    Routes user input to the appropriate handler based on detected intent.
    Returns a dictionary with keys: 'html', 'status', and optional 'meta'.
    """
    try:
        intent = detect_intent(message)

        if intent == "daily_workflow":
            return appointment_handler.handle(message)

        elif intent == "client_management":
            return client_handler.handle(message)

        elif intent == "smart_reminders":
            return reminders_handler.handle(message)

        elif intent == "sales_reports":
            return report_handler.handle(message)

        elif intent == "notes_followup":
            return notes_handler.handle(message)

        elif intent == "other_tools":
            return other_tools_handler.handle(message)

        else:
            return {
                "html": f"<p>🤖 I'm still learning! I couldn't understand your request:<br><i>{message}</i></p>"
                        f"<p>Please try rephrasing it or use one of the available sections.</p>",
                "status": "fallback"
            }

    except Exception as e:
        return {
            "html": f"<p>⚠️ Internal error while processing: <br><code>{str(e)}</code></p>",
            "status": "error"
        }

@app.route("/section/workflow")
def section_workflow():
    return jsonify(appointment_handler.handle_appointment_request())