#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()

    commande_id = request.form.get('idCommande')

    mycursor.execute("SELECT * FROM etat;")
    etats = mycursor.fetchall()

    mycursor.execute("SELECT * FROM user;")
    users = mycursor.fetchall()

    if commande_id == None:
        mycursor.execute("SELECT * FROM commande INNER JOIN etat ON commande.etat_id = etat.etat_id INNER JOIN user ON commande.user_id = user.user_id;")
        commandes = mycursor.fetchall()
        return render_template('admin/commandes/show.html', commandes=commandes, etats=etats, users=users)

    mycursor.execute("SELECT * FROM commande INNER JOIN etat ON commande.etat_id = etat.etat_id INNER JOIN user ON commande.user_id = user.user_id;")
    commandes = mycursor.fetchall()

    mycursor.execute("SELECT * FROM ligne_commande INNER JOIN meuble ON ligne_commande.meuble_id = meuble.meuble_id WHERE commande_id = %s;", (commande_id))
    articles_commande = mycursor.fetchall()

    return render_template('admin/commandes/show.html', commandes=commandes, articles_commande=articles_commande, etats=etats, users=users)


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('idCommande')
    print(commande_id)
    etat = request.form.get('changerEtat')
    print(etat)

    mycursor.execute("UPDATE commande SET etat_id = %s WHERE commande_id = %s;", (etat, commande_id))
    get_db().commit()
    return redirect('/admin/commande/show')
