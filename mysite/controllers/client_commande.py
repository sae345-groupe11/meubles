#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    prix_total = request.form.get('prixTotal')
    client_id = session['user_id']
    mycursor.execute("SELECT * FROM panier INNER JOIN meuble ON panier.meuble_id = meuble.meuble_id WHERE panier.user_id = %s", (client_id))
    items_panier = mycursor.fetchall()

    if items_panier is None:
        flash('Votre panier est vide...')
        return redirect(url_for('client_article_show'))

    nbr_articles = 0
    for item in items_panier:
        mycursor.execute("SELECT quantite FROM panier WHERE panier_id = %s;", (item['panier_id']))
        tmp = mycursor.fetchone()
        nbr_articles += tmp['quantite']

    mycursor.execute("INSERT INTO commande(date_achat, prix_total, nbr_articles, user_id, etat_id) VALUES(%s, %s, %s, %s, %s);", (datetime.date.today(), prix_total, nbr_articles, client_id, 1))
    mycursor.execute("SELECT last_insert_id() AS last_insert_id;")
    commande_id = mycursor.fetchone()

    for item in items_panier:
        mycursor.execute("INSERT INTO ligne_commande(commande_id, meuble_id, prix_unit, quantite) VALUES(%s, %s, %s, %s);", (commande_id['last_insert_id'], item['meuble_id'], item['prix_unit'], item['quantite']))
        mycursor.execute("DELETE FROM panier WHERE user_id = %s AND meuble_id = %s;", (client_id, item['meuble_id']))

    get_db().commit()
    flash(u'Commande ajoutée')
    return redirect('/client/meuble/show')
    #return redirect(url_for('client_index'))


@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()

    commande_id = request.form.get('idCommande')

    if commande_id == None:
        mycursor.execute("SELECT * FROM commande INNER JOIN etat ON commande.etat_id = etat.etat_id WHERE user_id = %s;", (session['user_id']))
        commandes = mycursor.fetchall()
        return render_template('client/commandes/show.html', commandes=commandes)

    mycursor.execute("SELECT * FROM commande INNER JOIN etat ON commande.etat_id = etat.etat_id WHERE user_id = %s;", (session['user_id']))
    commandes = mycursor.fetchall()
    mycursor.execute("SELECT * FROM ligne_commande INNER JOIN meuble ON ligne_commande.meuble_id = meuble.meuble_id WHERE commande_id = %s;", (commande_id))
    articles_commande = mycursor.fetchall()
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande)

