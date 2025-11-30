import os
from flask import Blueprint, request, jsonify, current_app
from app.recommender import Recommender

api_bp = Blueprint("api", __name__, url_prefix="")

_recommender = None

def get_recommender():
    global _recommender
    if _recommender is None:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        artifacts = os.path.join(root, 'data', 'processed')
        _recommender = Recommender(artifacts_path=artifacts)
    return _recommender

@api_bp.route("/recommend", methods=["GET"])
def recommend_by_title():
    title = request.args.get("title", "").strip()
    try:
        n = int(request.args.get("n", 5))
    except:
        n = 5
    if not title:
        return jsonify({"error": "query param 'title' required"}), 400
    try:
        recs = get_recommender().recommend_by_title(title, n)
        return jsonify({"query": title, "recommendations": recs})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        current_app.logger.exception("Unexpected error")
        return jsonify({"error": "internal server error"}), 500

@api_bp.route("/recommend_text", methods=["POST"])
def recommend_by_text():
    payload = request.get_json(silent=True) or {}
    plot = payload.get("plot", "") or payload.get("text", "")
    try:
        n = int(payload.get("n", 5))
    except:
        n = 5
    if not plot:
        return jsonify({"error": "JSON body must include 'plot' (string)"}), 400
    try:
        recs = get_recommender().recommend_by_plot(plot, n)
        return jsonify({"query_snippet": plot[:120], "recommendations": recs})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error")
        return jsonify({"error": "internal server error"}), 500
