from urllib.parse import quote

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)


WHATSAPP_PRIMARY = "5555999628003"
WHATSAPP_SECONDARY = "555581450635"

main_bp = Blueprint("main", __name__)


def _whatsapp_url(text, number=WHATSAPP_PRIMARY):
    return (
        f"https://wa.me/{number}"
        f"?text={quote(text)}"
    )


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/trabalhe-conosco")
def trabalhe_conosco():
    candidature_url = current_app.config.get("CANDIDATURE_URL", "")
    candidature_email = current_app.config.get("CANDIDATURE_EMAIL", "")

    return render_template(
        "trabalhe-conosco.html",
        candidature_url=candidature_url,
        candidature_email=candidature_email,
    )


@main_bp.route("/contato", methods=["POST"])
def contato():
    nome = request.form.get("nome", "").strip()
    whatsapp = request.form.get("whatsapp", "").strip()
    email = request.form.get("email", "").strip()
    mensagem = request.form.get("mensagem", "").strip()
    interesse = request.form.get("interesse", "").strip()

    if not all([nome, whatsapp, email, mensagem]):
        flash("Preencha todos os campos obrigatórios.", "error")
        return redirect(url_for("main.home") + "#contato")

    text = (
        f"Olá, meu nome é {nome}.\n"
        f"WhatsApp: {whatsapp}\n"
        f"E-mail: {email}\n"
        + (f"Interesse: {interesse}\n" if interesse else "")
        + f"\n{mensagem}"
    )

    return redirect(_whatsapp_url(text))


@main_bp.route("/consulta", methods=["POST"])
def consulta():
    email = request.form.get("email", "").strip()

    if not email:
        flash("Informe um e-mail para consulta.", "error")
        return redirect(url_for("main.home") + "#rodape")

    text = f"Gostaria de mais informações. Meu e-mail: {email}"
    return redirect(_whatsapp_url(text))


@main_bp.route("/candidatura", methods=["POST"])
def candidatura():
    candidature_url = current_app.config.get("CANDIDATURE_URL", "")

    if candidature_url:
        return redirect(candidature_url)

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    telefone = request.form.get("telefone", "").strip()
    mensagem = request.form.get("mensagem", "").strip()

    if not all([nome, email, telefone, mensagem]):
        flash("Preencha todos os campos para se candidatar.", "error")
        return redirect(url_for("main.trabalhe_conosco") + "#candidatura")

    text = (
        f"Candidatura — Trabalhe Conosco\n"
        f"Nome: {nome}\n"
        f"E-mail: {email}\n"
        f"Telefone: {telefone}\n\n"
        f"{mensagem}"
    )

    return redirect(_whatsapp_url(text))
