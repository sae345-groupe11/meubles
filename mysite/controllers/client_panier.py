#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import datetime

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    meuble_id = request.form.get('idMeuble')

    panier_id = request.form.get('idPanier')
    quantite = request.form.get('nbrMeubles')

    mycursor.execute("SELECT * FROM panier WHERE meuble_id = %s;", (meuble_id))
    is_in_panier = mycursor.fetchone()

    if panier_id == None:
        if is_in_panier == None:
            mycursor.execute("INSERT INTO panier(date_ajout, quantite, user_id, meuble_id) VALUES(%s, %s, %s, %s);", (datetime.date.today(), quantite, session['user_id'], meuble_id))
            mycursor.execute("UPDATE meuble SET stock = stock - %s WHERE meuble_id = %s;", (quantite, meuble_id))
            get_db().commit()
        else:
            mycursor.execute("UPDATE meuble SET stock = stock - %s WHERE meuble_id = %s;", (quantite, meuble_id))
            mycursor.execute("UPDATE panier SET quantite = quantite + %s WHERE panier_id = %s AND user_id;", (quantite, is_in_panier['panier_id'], session['user_id']))
            get_db().commit()
    else:
        mycursor.execute("SELECT stock FROM meuble WHERE meuble_id = %s;", (meuble_id))
        is_vide = mycursor.fetchone()
        if is_vide['stock'] == 0:
            flash('Meubles indisponibles pour l\'instant.')
            return redirect(url_for('client_article.client_article_show'))
        mycursor.execute("UPDATE meuble SET stock = stock - %s WHERE meuble_id = %s;", (quantite, meuble_id))
        mycursor.execute("UPDATE panier SET quantite = quantite + %s WHERE panier_id = %s AND user_id = %s;", (quantite, panier_id, session['user_id']))
        get_db().commit()
    return redirect('/client/meuble/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    meuble_id = request.form.get('idMeuble')
    panier_id = request.form.get('idPanier')
    quantite = int(request.form.get('nbrMeubles'))

    if quantite >= 2:
        mycursor.execute("UPDATE meuble SET stock = stock + 1 WHERE meuble_id = %s;", (meuble_id))
        mycursor.execute("UPDATE panier SET quantite = quantite - 1 WHERE panier_id = %s AND user_id = %s;", (panier_id, session['user_id']))
        get_db().commit()
    else:
        mycursor.execute("UPDATE meuble SET stock = stock + 1 WHERE meuble_id = %s;", (meuble_id))
        mycursor.execute("DELETE FROM panier WHERE panier_id = %s AND user_id = %s;", (panier_id, session['user_id']))
        get_db().commit()
    return redirect('/client/meuble/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()

    mycursor.execute("SELECT panier_id FROM panier;")
    ids = mycursor.fetchall()

    mycursor.execute("SELECT COUNT(*) AS nbrLignes FROM panier;")
    nbrLignes = mycursor.fetchone()
    nbrLignes = nbrLignes['nbrLignes']

    liste_ids = []

    for i in range(nbrLignes):
        id = ids[i]
        id = id['panier_id']
        liste_ids.append(id)

    for i in liste_ids:
        mycursor.execute("SELECT quantite FROM panier WHERE panier_id = %s AND user_id = %s", (i, session['user_id']))
        quantite = mycursor.fetchone()
        quantite = quantite['quantite']

        mycursor.execute("SELECT meuble_id FROM panier WHERE panier_id = %s AND user_id = %s", (i, session['user_id']))
        meuble_id = mycursor.fetchone()
        meuble_id = meuble_id['meuble_id']

        mycursor.execute("UPDATE meuble SET stock = stock + %s WHERE meuble_id = %s;", (quantite, meuble_id))
        mycursor.execute("DELETE FROM panier WHERE panier_id = %s AND user_id = %s;", (i, session['user_id']))
    get_db().commit()
    return redirect('/client/meuble/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    meuble_id = request.form.get('idMeuble')
    panier_id = request.form.get('idPanier')
    quantite = request.form.get('nbrMeubles')

    mycursor.execute("UPDATE meuble SET stock = stock + %s WHERE meuble_id = %s;", (quantite, meuble_id))
    mycursor.execute("DELETE FROM panier WHERE panier_id = %s AND user_id = %s;", (panier_id, session['user_id']))
    get_db().commit()
    return redirect('/client/meuble/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    mycursor = get_db().cursor()

    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    if len(filter_word) < 2:
        flash('Veuillez rentrer au moins 2 caractères pour la recherche par nom.')
        return redirect('/client/meuble/show')

    if filter_prix_min == "" or filter_prix_max == "":
        flash('Veuillez rentrer un prix minimum et un prix maximum pour la recherche par prix.')
        return redirect('/client/meuble/show')

    if filter_types == []:
        flash('Veuillez cocher au moins 1 catégorie pour la recherche par types.')
        return redirect('/client/meuble/show')

    session['filter_word'] = filter_word
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    session['filter_types'] = filter_types
    return redirect('/client/meuble/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/meuble/show')
    #return redirect(url_for('client_index'))

