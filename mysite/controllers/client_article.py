#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/meuble/show')      # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    filter_word = session.get('filter_word')
    filter_prix_min = session.get('filter_prix_min')
    filter_prix_max = session.get('filter_prix_max')
    filter_types = session.get('filter_types')

    # filtre nom + prix + types
    if filter_word != None and (filter_prix_min != None and filter_prix_max != None) and filter_types != []:
        mycursor.execute("SELECT * FROM meuble WHERE nom LIKE %s AND prix_unit BETWEEN %s AND %s AND type_meuble_id IN %s;", (filter_word + "%", filter_prix_min, filter_prix_max, filter_types))
        meubles = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM meuble;")
        meubles = mycursor.fetchall()

    mycursor.execute("SELECT * FROM type_meuble;")
    types_meuble = mycursor.fetchall()

    mycursor.execute("SELECT * FROM panier INNER JOIN meuble ON panier.meuble_id = meuble.meuble_id WHERE user_id = %s;", (session['user_id']))
    meubles_panier = mycursor.fetchall()

    mycursor.execute("SELECT SUM(prix_unit * quantite) AS addition FROM panier INNER JOIN meuble ON panier.meuble_id = meuble.meuble_id WHERE user_id = %s;", (session['user_id']))
    prix_total = mycursor.fetchone()
    return render_template('client/boutique/panier_article.html', meubles=meubles, meublesPanier=meubles_panier, prix_total=prix_total, itemsFiltre=types_meuble)

@client_article.route('/client/meuble/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()
    article=None
    commentaires=None
    commandes_articles=None
    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires, commandes_articles=commandes_articles)