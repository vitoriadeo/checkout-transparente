from flask import Blueprint, render_template, flash, redirect, url_for, session, request

section = Blueprint("main", __name__)


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


# @section.route("/pay", method=['POST'])
# def pay():
#     return


@section.route("/checkout")  # página /get
def checkout():
    if 'preco' not in session:
        return redirect(url_for('main.product'))
    return render_template("checkout.html")


@section.route("/order-placed")  # página /get
def order_placed():
    return render_template("order-placed.html")


# @section.route("/webhook-asaas", method=['POST'])
# def webhook_asaas():
#     return
