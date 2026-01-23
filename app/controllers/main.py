from flask import Blueprint, render_template, flash, redirect, url_for, session, request
import logging
from requests.exceptions import HTTPError
from ..services.asaas_service import cria_ou_consulta_cliente


section = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


@section.route("/product")  # página /get
def product():
    return render_template("product.html")


@section.route("/add-cart", methods=["POST"])
def add_cart():
    preco = request.form.get("preco")
    quantidade = request.form.get("quantidade")

    session["preco"] = preco
    session["quantidade"] = quantidade

    return redirect(url_for("main.checkout"))


@section.route("/clear-cart", methods=["POST"])
def clear_cart():
    session.clear()
    flash("Sua cesta de compras está vazia", "info")
    return redirect(url_for("main.product"))


@section.route("/pay", methods=["POST"])
def pay():
    dados_pessoais = {
        "name": request.form.get("nome"),
        "email": request.form.get("email"),
        "cpfCnpj": request.form.get("id"),
        "mobilePhone": request.form.get("telefone"),
        "postalCode": request.form.get("cep"),
        "addressNumber": request.form.get("numero"),
    }

    try:
        customer_id = cria_ou_consulta_cliente(dados_pessoais)

        payment_method = request.form.get("payment_method")

        if payment_method == 'CREDIT':
            pass
        elif payment_method == 'PIX':
            pass
        elif payment_method == 'BOLETO':
            pass
        else:
            logger.info(f"Forma de pagamento diferente do esperado. {payment_method}")
            flash("Houve um problema com a forma de pagamento. Verifique e tente novamente.", "error")
            return redirect(url_for('main.checkout'))

    except HTTPError as e:
        logger.warning(f"Erro 401 ou 400 - response Asaas")
        flash("Houve um problema com os dados do pagamento. Verifique e tente novamente.", "error")
        return redirect(url_for('main.checkout'))
    
    except Exception as e:
        logger.error(f"Erro interno não esperado: {e}")
        flash("Erro interno do servidor. Tente mais tarde.", "error")
        return redirect(url_for('main.checkout'))


@section.route("/checkout")  # página /get
def checkout():
    if "preco" not in session:
        return redirect(url_for("main.product"))
    return render_template("checkout.html")


@section.route("/order-placed")  # página /get
def order_placed():
    return render_template("order-placed.html")


# @section.route("/webhook-asaas", method=['POST'])
# def webhook_asaas():
#     return
