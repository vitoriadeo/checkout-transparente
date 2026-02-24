from flask import Blueprint, render_template, flash, redirect, url_for, session, request
import logging
from ..services.cobranca import *
from ..services import checkout_service

section = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


@section.route("/product")  # página /get
def product():
    return render_template("product.html")


@section.route("/add-cart", methods=["POST"])
def add_cart():
    preco = request.form.get("preco")
    quantidade = request.form.get("quantidade")

    session["preco"] = float(preco)
    session["quantidade"] = int(quantidade)

    session["valor_total"] = session["preco"] * session["quantidade"]

    return redirect(url_for("main.checkout"))


@section.route("/clear-cart", methods=["POST"])
def clear_cart():
    session.clear()
    flash("Sua cesta de compras está vazia", "info")
    return redirect(url_for("main.product"))


@section.route("/pay", methods=["POST"])
def pay():
    dados_formulario = request.form.to_dict()
    valor_total = session.get("valor_total")

    resultado = checkout_service.processar_pagamento(dados_formulario, valor_total)

    if not resultado["sucesso"]:
        flash(resultado["erro"], "error")
        return redirect(url_for("main.checkout"))

    tipo = resultado["tipo"]
    session[f"dados_{tipo}"] = resultado["dados"]
    
    return redirect(url_for(f"main.{tipo}"))


@section.route("/pay/pix", methods=["GET"])
def pix():
    dados = session.get("dados_pix")

    if not dados:
        return redirect(url_for("main.checkout"))

    return render_template("billing/pix.html", dados=dados)


@section.route("/pay/boleto", methods=["GET"])
def boleto():
    dados = session.get("dados_boleto")

    if not dados:
        return redirect(url_for("main.checkout"))

    return render_template("billing/boleto.html", dados=dados)


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
